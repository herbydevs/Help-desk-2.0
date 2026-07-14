<template>
  <div class="activation-page">
    <p v-if="status" :class="statusClass">{{ status }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted,computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const status = ref('')
const route = useRoute()
const router = useRouter()


// Determine color based on status text
const statusClass = computed(() => {
  if (status.value.toLowerCase().includes('success')) {
    return 'text-green-600'
  }
  if (status.value.toLowerCase().includes('failed') || status.value.toLowerCase().includes('invalid')) {
    return 'text-red-600'
  }
  return 'text-gray-700'
})


onMounted(async () => {
  console.log("Started!!")
  const token = route.query.token
  if (!token) {
    status.value = 'Invalid activation link'
    return
  }

  try {
    const res = await fetch(`/api/activate/${token}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
  
    
    status.value = await res.text()
    //router.push('/login')
  } catch (e) {
    status.value = 'Activation failed'
  }
})
</script>
<style scoped>
.activation-page {
  padding: 2rem;
  text-align: center;
}
</style>
