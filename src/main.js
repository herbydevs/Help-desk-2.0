import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

// Import Vue Router
import router from './router'

// Create and mount app
const app = createApp(App)
app.use(router)
app.mount('#app')
