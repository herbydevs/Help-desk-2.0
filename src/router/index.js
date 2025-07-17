import { createRouter, createWebHistory } from 'vue-router'
import Client from '../components/client.vue'
import TicketList from '../components/ticket_list.vue'
import UserManagement from '../components/userManagement.vue'
import Login from '../components/login.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes: [
    {
      path: '/',
      name: 'Client',
      component: Client
    },

    
    {
      path: '/tickets',
      name: 'TicketList',
      component: TicketList
    },
    {
      path: '/user-management',
      name: 'UserManagement',
      component: UserManagement


      
    },

    {
      path: '/login',
      name: 'login',
      component: Login


      
    },

    { path: '/:pathMatch(.*)*', redirect: '/' }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const isLoggedIn = !!token;

  // Allow access to login page without token
  if (to.path === '/login') {
    next();
  } else if (!isLoggedIn) {
    // Redirect all other routes to /login if not logged in
    next('/login');
  } else {
    next(); // allow navigation
  }
});

export default router
