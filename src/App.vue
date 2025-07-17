
<script setup>
//test commit comment
//dev branch
import { ref } from 'vue';

import { RouterView } from 'vue-router';


const isLoading = ref(false);
const isLoggedIn = ref(false);
const handleLogout = () => {
            localStorage.removeItem('token');
            window.location.href = '/help-desk/login';
        };

</script>

<template>
  <div class="container" v-cloak>
    <nav class="nav-bar">
      <h1>Help Desk System</h1>
      <button @click="handleLogout"  v-if="isloggedIn" class="logout-button">Logout</button>
    </nav>
    <div class="content">
      <RouterView v-slot="{ Component }">
        <Transition mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </div>
  </div>
</template>


<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f8f9fa;
  margin-bottom: 2rem;
  border-radius: 8px;
}

.logout-btn {
  padding: 8px 16px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #c82333;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.role-badge {
  padding: 4px 8px;
  border-radius: 4px;
  background-color: #6c757d;
  color: white;
  font-size: 0.875rem;
}

.role-badge.admin {
  background-color: #28a745;
}

.content {
  display: block;
  max-width: 800px;
  margin: 0 auto;
}

[v-cloak] {
  display: none;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

/* Add transition styles */
.v-enter-active,
.v-leave-active {
  transition: opacity 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}

button {
    width: 100%;
    max-width: fit-content;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin: 10px 0;
}

button:hover {
    background-color: #0056b3;
}

</style>