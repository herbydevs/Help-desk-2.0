
<script setup>
import NavBar from './components/UI/NavBar.vue';
import Sidebar from './components/UI/sidebar.vue';

</script>

<template>
 <div class="container" v-cloak>

    <div class="content">
   
      <RouterView/>
    </div>
  </div>
</template>


<style scoped>


.sidebar {
  width: 220px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  background: #fff;
  padding: 32px 16px;
  border-right: 1px solid #eee;
  box-shadow: 2px 0 8px rgba(0,0,0,0.04);
  border-radius: 0 16px 16px 0;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
}

.sidebar li {
  margin-bottom: 18px;
  width: 100%;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  color: #333;
  font-weight: 500;
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
}

.sidebar-link i {
  font-size: 1.2rem;
  color: #007bff;
  min-width: 24px;
  text-align: center;
}

.sidebar-link:hover,
.sidebar-link.router-link-active {
  background: #f0f4ff;
  color: #007bff;
}

.sidebar-link.router-link-active i {
  color: #0056b3;
}


.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
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