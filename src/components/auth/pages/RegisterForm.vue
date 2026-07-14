<template>
  <div class="login-container">
    
  <form class="login-form" @submit.prevent="register">

          <h2>Registration Form</h2>

    <div class="input-group">
      <input v-model="name" type="text" placeholder="Name" required />
    </div>
    <div class="input-group">
        <input v-model="email" type="email" placeholder="Email" required />
    </div>
    <div class="input-group">
      <input v-model="password" type="password" placeholder="Password" required />
    </div>
    <div class="input-button-group">
      <button type="submit">Register</button>
    </div>
            <RouterLink to="/login">Login</RouterLink>

    <p v-if="message">{{ message }}</p>
  </form>
  </div>
</template>



<script setup>
import { ref } from 'vue'

const name = ref('')
const email = ref('')
const password = ref('')
const message = ref('')

const register = async () => {
  try {
    const response = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: name.value,
        email: email.value,
        password: password.value
      })
    })
    message.value = await response.text()
  } catch (e) {
    message.value = 'An error occurred'
  }
}
</script>

<style scoped>
.form-group {
    margin-bottom: 15px;
}

.login-container {

 max-width: 500px;
  padding: 10px;
  display: flex;
  margin: auto;
}


.login-form {
  background: #ffffff;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  width: 100%;
}

.login-form h2 {
  margin-bottom: 20px;
  text-align: center;
  color: #333;
}

.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: bold;
  color: #555;
}

.input-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  box-sizing: border-box;
}



.input-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #1abc9c;
  border: none;
  color: white;
  font-size: 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background-color: #34495e;
}

.signup-link {
  margin-top: 15px;
  text-align: center;
  font-size: 14px;
}

.signup-link a {
  color: #4e54c8;
  text-decoration: none;
}
.input-button-group{
      margin-bottom: 15px;

}
.input-button-group button{
    margin-bottom: 5px;
}
</style>