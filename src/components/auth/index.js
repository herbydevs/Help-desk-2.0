import activate from './pages/Activate.vue'
import login from './pages/login.vue'
import register from './pages/RegisterForm.vue'


export default [
  {
    name: "login",
    path: "login",
    component: login
  },
  {
    name: "activate",
    path: "activate",
    component: activate
  },
  {
    name: "register",
    path: "register",
    component: register
  }

]
