import { createRouter, createWebHistory } from 'vue-router'
//import Client from '../components/client.vue'
import TicketList from '../components/ticket_list.vue'
import UserManagement from '../components/userManagement.vue'
import Login from '../components/Login.vue'
// import InstitutionManagement from '../components/institutionManagement.vue'
// import EditInstitution from '../components/EditInstitution.vue'
import EditUser from '../components/EditUser.vue'
import ViewTicket from '../components/ViewTicket.vue'
import RegisterForm from '../components/RegisterForm.vue'
import ActivateView from '../components/Activate.vue'
import FequentlyAskedQuestions from '../components/FequentlyAskedQuestions.vue'
import IssueTypeManagement from '../components/IssueTypeManagement.vue'
import TicketStatusManagement from '../components/TicketStatusManagement.vue'
import institutionRoutes from '../components/institution_management'
import Default from '../components/views/MainTemplate.vue'
import clientRoutes from '../components/client'
import chatRoutes from '../components/chatbot'
import MainTemplate from '../components/views/MainTemplate.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes: [

      // {
      //     path: '/',
      //     component:Default,
      //     children: [
      //
      //     ]
      // },
      // example for using default views and other views when creating new routes

      {
      name: "chatbot",
      path: "/chatbot",
      component: MainTemplate,
      children: [
        ...chatRoutes
      ]
      },

      {
      name: "institutions",
      path: '/institutions',
      component: Default,
      children: [
        ...institutionRoutes
      ]
      },

     {
      path: '/',
      name: 'Client',
       component: Default,
       children: [
         ...clientRoutes
       ]
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
    // {
    //   path: '/institution-management',
    //   name: 'InstitutionManagement',
    //   component: InstitutionManagement
    // },
    //  {
    //   path: '/institutions/edit/:id',
    //   name: 'edit-institution',
    //   component: EditInstitution
    // },
    {
      path: '/users/edit/:id',
      name: 'edit-user',
      component: EditUser
    },
     {
      path: '/tickets/view/:id',
      name: 'view-ticket',
      component: ViewTicket
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterForm
    },
    {
      path: '/activate',
      name: 'activate-account',
      component: ActivateView
    },
     {
      path: '/frequently-asked-questions',
      name: 'frequently-asked-questions',
      component: FequentlyAskedQuestions
    },
    {
      path: '/issue-types',
      name: 'issue-types',
      component: IssueTypeManagement
    },
     {
      path: '/ticket-statuses',
      name: 'ticket-statuses',
      component: TicketStatusManagement
      },
    { path: '/:pathMatch(.*)*', redirect: '/' }
  ]
})


export default router
