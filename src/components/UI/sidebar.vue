<template>

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
</nav>

</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';

const auth = useAuthStore();
const router = useRouter();
const userEmail = computed(() => auth.user?.email);
const isLoggedIn = computed(() => auth.isLoggedIn);
const isAdmin = computed(() => auth.user?.admin);




const goToUsers = () => router.push('/user-management');
const goToInstitutions = () => router.push('/institutions/manage');
const goToTickets = () => router.push('/tickets');
const goToSubmitTicket = () => router.push('/help-desk/');
const goToFequentlyAskedQuestions = () => router.push('/frequently-asked-questions');
const goToIssueTypes = () => router.push('/issue-types');
const goToTicketStatuses = () => router.push('/ticket-statuses');
</script>

<style scoped>

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
</style>
