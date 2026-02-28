<script setup lang="ts">
const auth = useAuthStore()
const users = ref([])
const isLoading = ref(true)

const fetchUsers = async () => {
  try {
    const response = await $fetch('/api/v1/admin/users', {
      headers: {
        Authorization: `Bearer ${auth.token}`
      }
    })
    users.value = response
  } catch (error) {
    console.error('Failed to fetch users', error)
  } finally {
    isLoading.value = false
  }
}

const toggleActive = async (userId: string) => {
  try {
    const response = await $fetch(`/api/v1/admin/users/${userId}/toggle-active`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${auth.token}`
      }
    })
    // Update local state
    const index = users.value.findIndex(u => u.id === userId)
    if (index !== -1) {
      users.value[index] = response
    }
  } catch (error) {
    console.error('Failed to toggle user status', error)
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 p-8">
    <div class="max-w-6xl mx-auto">
      <header class="flex justify-between items-center mb-12">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
            Tenant Administration
          </h1>
          <p class="text-slate-400 mt-2">Manage your organization's members and licenses</p>
        </div>
        <div class="flex gap-4">
          <div class="bg-indigo-500/10 border border-indigo-500/20 px-4 py-2 rounded-xl text-sm">
            <span class="text-indigo-400 font-bold">{{ users.length }}</span> 
            <span class="text-slate-400 ml-1">Total Users</span>
          </div>
        </div>
      </header>

      <div class="bg-slate-900/50 rounded-3xl border border-slate-800 backdrop-blur-xl overflow-hidden shadow-2xl">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-800/50 border-b border-slate-800">
              <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-slate-500">Full Name</th>
              <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-slate-500">Email</th>
              <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-slate-500">Role</th>
              <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-slate-500">Status</th>
              <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-slate-500 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/50">
            <tr v-if="isLoading" v-for="i in 3" :key="i" class="animate-pulse">
              <td colspan="5" class="px-6 py-8 h-16 bg-slate-800/10"></td>
            </tr>
            <tr v-else v-for="user in users" :key="user.id" class="hover:bg-slate-800/30 transition-colors">
              <td class="px-6 py-4">
                <div class="font-medium">{{ user.full_name || 'Anonymous' }}</div>
              </td>
              <td class="px-6 py-4 text-slate-400 font-mono text-sm">
                {{ user.email }}
              </td>
              <td class="px-6 py-4">
                <span class="px-2 py-1 bg-slate-800 rounded-md text-[10px] uppercase font-bold text-slate-400 border border-slate-700">
                  {{ user.role }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                  <div :class="user.is_active ? 'bg-emerald-500' : 'bg-rose-500'" class="w-2 h-2 rounded-full"></div>
                  <span class="text-xs">{{ user.is_active ? 'Active' : 'Deactivated' }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-right">
                <button 
                  @click="toggleActive(user.id)"
                  class="text-xs px-3 py-1.5 rounded-lg border transition-all"
                  :class="user.is_active ? 'border-rose-500/30 text-rose-400 hover:bg-rose-500/10' : 'border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/10'"
                >
                  {{ user.is_active ? 'Deactivate' : 'Activate' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="!isLoading && users.length === 0" class="p-12 text-center text-slate-500">
          No users found in this tenant.
        </div>
      </div>
    </div>
  </div>
</template>
