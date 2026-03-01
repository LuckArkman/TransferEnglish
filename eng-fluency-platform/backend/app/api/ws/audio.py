from fastapi import WebSocket, WebSocketDisconnect
import json
import base64
import time
import io
from app.services.ai.asr_service import asr_service
from app.services.ai.chat_service import chat_service
from app.services.ai.tts_service import tts_service
from app.services.ai.adaptation_logic import adaptation_logic
from app.services.ai.scenario_manager import scenario_manager
from app.services.ai.interruption_engine import interruption_engine
from app.services.ai.pressure_engine import pressure_engine
from typing import Dict, List
from app.schemas.analytics import FluencySessionBase

class AudioSocketManager:
    def __init__(self):
        # active_connections maps tenant_id to a list of sockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, tenant_id: str):
        await websocket.accept()
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = []
        self.active_connections[tenant_id].append(websocket)

    def disconnect(self, websocket: WebSocket, tenant_id: str):
        if tenant_id in self.active_connections:
            self.active_connections[tenant_id].remove(websocket)
            if not self.active_connections[tenant_id]:
                del self.active_connections[tenant_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_tenant(self, message: str, tenant_id: str):
        if tenant_id in self.active_connections:
            for connection in self.active_connections[tenant_id]:
                await connection.send_text(message)

    async def handle_audio_stream(self, websocket: WebSocket, tenant_id: str):
        """
        Main loop for handling binary audio data and control messages.
        Orchestrates the full cycle: User Audio -> Transcription -> LLM -> TTS -> Client
        """
        conversation_history = []
        current_scenario_id = None
    
        # Session tracking for adaptation (Sprint 16)
        session_metrics = FluencySessionBase(
            ifp_score=60.0, # Initial "Functional" baseline
            accuracy_avg=70.0,
            fluency_avg=70.0,
            prosody_avg=70.0,
            total_words=0,
            duration_seconds=0.0,
            response_latency_avg=1.0
        )
    
        system_mod = ""
        full_audio_accumulator = bytearray()
        # Store the first WebM chunk as the stream header so we can prepend it
        # when the buffer is reset (WebM requires the initial cluster headers)
        audio_header = bytearray()

        async def process_buffer():
            nonlocal full_audio_accumulator
            if not full_audio_accumulator or websocket.client_state.value != 1: 
                return

            try:
                data_to_process = bytes(full_audio_accumulator)

                # If accumulated bytes don't start with EBML header but we have one stored,
                # prepend it so the WebM container is always valid
                if audio_header and not data_to_process.startswith(b'\x1a\x45\xdf\xa3'):
                    data_to_process = bytes(audio_header) + data_to_process

                # Send raw bytes directly to Gemini — no ffmpeg conversion needed
                transcription = await asr_service.transcribe(data_to_process)
                
                if transcription.text.strip():
                    await websocket.send_json({
                        "type": "transcription",
                        "text": transcription.text
                    })

                    # Chat Logic
                    chat_history_mapped = [{"role": msg["role"], "content": msg["content"]} for msg in conversation_history]
                    ai_response_text = await chat_service.get_response(
                        chat_history_mapped, 
                        transcription.text,
                        system_modifier=system_mod
                    )
                    
                    conversation_history.append({"role": "user", "content": transcription.text})
                    conversation_history.append({"role": "assistant", "content": ai_response_text})

                    # TTS
                    audio_response = await tts_service.generate_speech(ai_response_text)
                    
                    if websocket.client_state.value == 1:
                        await websocket.send_json({
                            "type": "ai_response",
                            "text": ai_response_text
                        })
                        
                        if audio_response:
                            await websocket.send_json({
                                "type": "audio_response",
                                "audio": base64.b64encode(audio_response).decode('utf-8')
                            })
            except Exception as e:
                print(f"Error in process_buffer: {e}")
            finally:
                full_audio_accumulator = bytearray()

        try:
            # Initial system mod calculation
            system_mod = adaptation_logic.get_llm_instruction(session_metrics)
            
            while websocket.client_state.value == 1:
                data = await websocket.receive()
                
                if "bytes" in data:
                    audio_chunk = data["bytes"]
                    
                    # On the very first WebM chunk, store the entire chunk as the stream header.
                    # WebM files require EBML + Segment headers to be decodable.
                    if len(audio_header) == 0 and audio_chunk.startswith(b'\x1a\x45\xdf\xa3'):
                        audio_header.extend(audio_chunk)

                    full_audio_accumulator.extend(audio_chunk)
                    
                    if len(full_audio_accumulator) > 500000: # Threshold auto-transcribe
                        await process_buffer()
                
                elif "text" in data:
                    message = json.loads(data["text"])
                    m_type = message.get("type")
                    
                    if m_type == "stop_recording":
                        await process_buffer()
                    elif m_type == "ping":
                        await websocket.send_json({"type": "pong"})
                    elif m_type == "set_scenario":
                        current_scenario_id = message.get("scenario_id")
                        conversation_history = []
                        # Refresh system prompt for new scenario
                        from app.core.db.session import SessionLocal
                        with SessionLocal() as db:
                            scenario_prompt = scenario_manager.get_scenario_prompt(db, current_scenario_id)
                            system_mod = f"{scenario_prompt}\n{adaptation_logic.get_llm_instruction(session_metrics)}"
                    elif m_type == "clear_history":
                        conversation_history = []
                    
        except WebSocketDisconnect:
            pass
        finally:
            self.disconnect(websocket, tenant_id)

audio_manager = AudioSocketManager()
