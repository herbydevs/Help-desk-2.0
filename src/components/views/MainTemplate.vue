<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';
import sidebar from '../UI/sidebar.vue'

const auth = useAuthStore();
const router = useRouter();
const userEmail = computed(() => auth.user?.email);
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
/*
const goToUsers = () => window.location.href = 'http://138.68.58.185/help-desk/user-management';
const goToInstitutions = () => window.location.href = 'http://138.68.58.185//help-desk/institution-management';
const goToTickets = () => window.location.href = 'http://138.68.58.185//help-desk/tickets';
const goToSubmitTicket = () => window.location.href = 'http://138.68.58.185//help-desk/';
const goToFequentlyAskedQuestions = () => window.location.href = 'http://138.68.58.185//help-desk/frequently-asked-questions';
const goToIssueTypes = () => window.location.href = 'http://138.68.58.185//help-desk/issue-types';
const goToTicketStatuses = () => window.location.href = 'http://138.68.58.185//help-desk/ticket-statuses';
*/

// const goToInstitutions = () => {
//   console.log("hello world")
// }

const goToUsers = () => router.push('/user-management');
const goToInstitutions = () => router.push('/institutions/manage');
const goToTickets = () => router.push('/tickets');
const goToSubmitTicket = () => router.push('/help-desk/');
const goToFequentlyAskedQuestions = () => router.push('/frequently-asked-questions');
const goToIssueTypes = () => router.push('/issue-types');
const goToTicketStatuses = () => router.push('/ticket-statuses');


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
        <img src="../assets/cardtp.png" alt="cardtp logo" class="logo" />
        <!--  <img src="../assets/vswift.png" alt="vswift logo" class="logo" />-->
        <div> <h2 class="title">Help Desk</h2></div>

      </div>

<!-- User email on the right -->
  <div v-if="isLoggedIn" class="topbar-user">
    <i class="pi pi-user"></i> {{ userEmail }}
  </div>

    </header>



    <!-- Overlay for mobile -->
    <div
      v-if="sidebarOpen"
      class="overlay"
      @click="closeSidebar"
    ></div>

    <!-- Sidebar -->
    <!-- <nav class="sidebar" :class="{ open: sidebarOpen }">
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
          <button class="sidebar-link" @click="goToIssueTypes">
            <i class="pi pi-objects-column"></i><span>Issue Types</span>
          </button>
        </li>
        <li v-if="isAdmin">
          <button class="sidebar-link" @click="goToTickets">
            <i class="pi pi-list-check"></i><span>Tickets</span>
          </button>
        </li>
        <li v-if="isAdmin">
          <button class="sidebar-link" @click="goToTicketStatuses">
            <i class="pi pi-list-check"></i><span>Ticket Statuses</span>
          </button>
        </li>
         <li>
          <button class="sidebar-link" @click="goToFequentlyAskedQuestions">
            <i class="pi pi-question"></i><span>FAQ</span>
          </button>
        </li>
        <li v-if="isLoggedIn">
          <button class="sidebar-link" @click="handleLogout">
            <i class="pi pi-sign-out"></i><span>Logout</span>
          </button>
        </li>
      </ul>
    </nav> -->
    <sidebar/>

    <!-- Main Content -->
    <main class="content">
      <router-view/>
    </main>
  </div>
</template>

<style scoped>
.title{
  color: black;
}
.layout {
  display: flex;
  min-height: 100vh;
}

.user-email {
  font-size: 0.9rem;
  opacity: 0.9;
  color: #007bff;
}

.topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  /*background: #007bff;*/
  background: #f8f9fa;

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
  color: #007bff;
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
   border-radius: 8px;
}

.sidebar-link:hover {
  background: #f0f4ff;
}
.sidebar-link i {
  font-size: 1.2rem;
  color: #007bff;
  min-width: 24px;
  text-align: center;
}
/* Main content */
.content {
  flex: 1; /* Take all available space */
  padding: 80px 20px 20px; /* Top padding accounts for fixed topbar */
  /*margin-left: 220px;  /*Matches sidebar width */
  margin-left: 20px;

  box-sizing: border-box;
  max-width: 100%;
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

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.topbar-user {
  font-size: 0.85rem;
  color: green;
  margin-left: auto;
}
@media (max-width: 768px) {
  .topbar-user {
    font-size: 0.75rem;
  }
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
    padding: 80px 5px 20px;
  }
}
</style>
