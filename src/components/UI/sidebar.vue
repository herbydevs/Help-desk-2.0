<template>

<nav class="sidebar" :class="{ open: sidebarOpen }">
  <ul>
      <li v-for="item in sidebarItems">
            <button class="sidebar-link" @click="item.action">
                <i :class="['pi', item.icon]"></i>
                <span>{{ item.label }}</span>
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
const sidebarItems = computed(() => {
  const rawItems = [
    { label: 'Users', icon: 'pi-users', action: goToUsers, show: isAdmin.value },
    { label: 'Submit a ticket', icon: 'pi-plus', action: goToSubmitTicket, show: true },
    { label: 'Institutions', icon: 'pi-building-columns', action: goToInstitutions, show: isAdmin.value },
    { label: 'Issue Types', icon: 'pi-objects-column', action: goToIssueTypes, show: isAdmin.value },
    { label: 'Tickets', icon: 'pi-list-check', action: goToTickets, show: isAdmin.value },
    { label: 'Ticket Statuses', icon: 'pi-list-check', action: goToTicketStatuses, show: isAdmin.value },
    { label: 'FAQ', icon: 'pi-question', action: goToFequentlyAskedQuestions, show: true },
    {label: 'chatbot', icon: '', action: goToChatbot, show: isLoggedIn.value},
    { label: 'Logout', icon: 'pi-sign-out', action: handleLogout, show: isLoggedIn.value }
  ]

  return rawItems.filter(item => item.show)
})



const goToUsers = () => router.push('/user-management');
const goToChatbot = () => router.push('/chatbot/chat');
const goToInstitutions = () => router.push('/institutions/manage');
const goToTickets = () => router.push('/tickets');
const goToSubmitTicket = () => router.push('/help-desk/');
const goToFequentlyAskedQuestions = () => router.push('/frequently-asked-questions');
const goToIssueTypes = () => router.push('/issue-types');
const goToTicketStatuses = () => router.push('/ticket-statuses');
const handleLogout = () => {auth.logout(), router.push('/login')}
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
