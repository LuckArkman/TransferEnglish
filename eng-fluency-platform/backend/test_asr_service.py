import os
import io
import asyncio
from app.services.ai.asr_service import asr_service

async def test_asr():
    print("Testing ASR with model:", asr_service.model.model_name)
    # Empty buffer just to test if the model call initializes correctly
    empty_buffer = io.BytesIO(b"") 
    try:
        res = await asr_service.transcribe(empty_buffer)
        print("Success, at least it didn't throw a 404!")
    except Exception as e:
        print(f"ASR Test Failure: {e}")

if __name__ == "__main__":
    asyncio.run(test_asr())
