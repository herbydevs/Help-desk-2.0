<script setup>
import { ref, onMounted } from 'vue';
import Client from './components/client.vue';
import Login from './components/login.vue';
import TicketList from './components/ticket_list.vue';

const isLoggedIn = ref(false);
const isAdmin = ref(false);

onMounted(() => {
  // Check if token exists in localStorage
  const token = localStorage.getItem('token');
  if (token) {
    isLoggedIn.value = true;
    // Check if user is admin from stored user data
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    isAdmin.value = userData.is_admin || false;
  }
});

const handleLoginSuccess = (userData) => {
  isLoggedIn.value = true;
  isAdmin.value = userData.is_admin || false;
  localStorage.setItem('userData', JSON.stringify(userData));
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('userData');
  isLoggedIn.value = false;
  isAdmin.value = false;
};
</script>

<template>
  <div class="container">
    <template v-if="!isLoggedIn">
      <Login @login-success="handleLoginSuccess" />
    </template>
    <template v-else>
      <nav class="nav-bar">
        <h1>Help Desk System</h1>
        <div class="user-info">
          <span class="role-badge" :class="{ admin: isAdmin }">
            {{ isAdmin ? 'Admin' : 'User' }}
          </span>
          <button @click="handleLogout" class="logout-btn">Logout</button>
        </div>
      </nav>
      <div class="content">
        <template v-if="isAdmin">
          <TicketList />
        </template>
        <template v-else>
          <Client />
        </template>
      </div>
    </template>
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
</style>