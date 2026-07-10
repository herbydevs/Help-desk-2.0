<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth.js';

const auth = useAuthStore();
const router = useRouter();

const isLoggedIn = computed(() => auth.isLoggedIn);
const isAdmin = computed(() => auth.user?.admin);

const sidebarOpen = ref(false); // For mobile toggle

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value;
};

const closeSidebar = () => {
  sidebarOpen.value = false;
};

const handleLogout = () => {
  auth.logout();
  router.push('/login');
};

const goToUsers = () => window.location.href = '/help-desk/user-management';
const goToInstitutions = () => window.location.href = '/help-desk/institution-management';
const goToTickets = () => window.location.href = '/help-desk/tickets';
const goToSubmitTicket = () => window.location.href = '/help-desk/';

// Optional: close menu on ESC key
const handleKeydown = (e) => {
  if (e.key === 'Escape' && sidebarOpen.value) closeSidebar();
};

onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
});
onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown);
});
</script>

<template>
  <div class="layout" v-cloak>
    <!-- Topbar -->
    <header class="topbar">
      <button class="hamburger" @click="toggleSidebar">☰</button>
      <div class="topbar-title">
        <img src="../../assets/cardtp.png" alt="cardtp logo" class="logo" />
        <img src="../../assets/vswift.png" alt="vswift logo" class="logo" />
      </div>
    </header>

    <!-- Overlay for mobile -->
    <div 
      v-if="sidebarOpen" 
      class="overlay" 
      @click="closeSidebar"
    ></div>

    <!-- Sidebar (refactor later useing a v-for and a array instead of 10 million list elements) -->

    <nav class="sidebar" :class="{ open: sidebarOpen }">
      <ul>
        <li v-if="isAdmin">
          <button class="sidebar-link" @click="goToUsers">
            <i class="pi pi-users"></i><span>Users</span>
          </button>
        </li>
        <li>
          <button class="sidebar-link" @click="goToSubmitTicket">
            <i class="pi pi-plus"></i><span>Submit a ticket</span>
          </button>
        </li>
        <li v-if="isAdmin">
          <button class="sidebar-link" @click="goToInstitutions">
            <i class="pi pi-building-columns"></i><span>Institutions</span>
          </button>
        </li>
        <li v-if="isAdmin">
          <button class="sidebar-link" @click="goToTickets">
            <i class="pi pi-list-check"></i><span>Tickets</span>
          </button>
        </li>
        <li v-if="isLoggedIn">
          <button class="sidebar-link" @click="handleLogout">
            <i class="pi pi-sign-out"></i><span>Logout</span>
          </button>
        </li>
      </ul>
    </nav>

    <!-- Main Content -->
    <main class="content">
      <slot></slot>
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: #007bff;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 1rem;
  z-index: 200;
}

.topbar-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  height: 40px;
}

.hamburger {
  font-size: 1.5rem;
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  margin-right: 1rem;
}

/* Sidebar */
.sidebar {
  position: fixed;
  top: 60px;
  left: 0;
  width: 220px;
  height: calc(100% - 60px);
  background: white;
  border-right: 1px solid #eee;
  padding: 1rem;
  overflow-y: auto;
  transition: transform 0.3s ease-in-out;
  z-index: 300;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: none;
  background: transparent;
  width: 100%;
  text-align: left;
  font-weight: 500;
  cursor: pointer;
}

.sidebar-link:hover {
  background: #f0f4ff;
}

/* Main content */
.content {
  flex: 1;
  margin-left: 220px;
  padding: 80px 20px 20px;
}

/* Overlay for mobile */
.overlay {
  position: fixed;
  top: 60px;
  left: 0;
  width: 100%;
  height: calc(100% - 60px);
  background: rgba(0, 0, 0, 0.4);
  z-index: 250;
}

/* Mobile & Tablet */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }
  .sidebar.open {
    transform: translateX(0);
  }
  .content {
    margin-left: 0;
    padding: 80px 20px 20px;
  }
}
</style>
