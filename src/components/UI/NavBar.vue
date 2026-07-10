<script setup>
import { useAuthStore } from '../../stores/auth.js';
//import { useAuthStore } from '@/stores/auth';
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { defineEmits } from 'vue';

const auth = useAuthStore();
const router = useRouter();
const emit = defineEmits(['logout']);

//const user = ref(null);
const isLoggedIn = computed(() => auth.isLoggedIn);
const userEmail = computed(() => auth.user?.email);



const handleLogout = () => {
  auth.logout();
  router.push('/login');
};
</script>

<template>
  <nav class="nav-bar">
    <h1>Help Desk System</h1>

    <div class="nav-right" v-if="isLoggedIn">
      <span class="user-email">Logged in as: {{ userEmail }}</span>
    <!--  <button @click="handleLogout" class="logout-button">Logout</button>-->
    </div>
  </nav>
</template>

<style scoped>
.nav-bar1 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
  color: #2c3e50;
  padding: 1rem;
  border: solid thin#DDD;
  border-radius: 10px;
}

.nav-bar{
      display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f8f9fa;
  margin-bottom: 2rem;
  border-radius: 8px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-button {
  background-color: #e74c3c;
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  cursor: pointer;
  border-radius: 4px;
}

.logout-button:hover {
  background-color: #c0392b;
}

.user-email {
  font-size: 0.9rem;
  opacity: 0.9;
}
</style>