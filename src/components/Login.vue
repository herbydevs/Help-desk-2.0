<template>
    <div class="login-form">
        <h2>Login</h2>
        <form @submit="handleLogin">
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="email" required />
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
            <button type="submit">Login</button>
        </form>
        <div v-if="error" class="error">{{ error }}</div>
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    name: 'Login',
    setup(_, { emit }) {
        const email = ref('');
        const password = ref('');
        const error = ref('');

        const handleLogin = async (event) => {
            event.preventDefault();
            try {
                const response = await fetch('http://localhost:8000/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email.value,
                        password: password.value,
                    }),
                });
                
                const data = await response.json();
                if (response.ok) {
                    localStorage.setItem('token', data.access_token);
                    emit('login-success', data.user); // Pass the user data including is_admin
                } else {
                    error.value = data.detail;
                }
            } catch (err) {
                error.value = 'Login failed. Please try again.';
            }
        };

        return {
            email,
            password,
            error,
            handleLogin
        };
    }
};
</script>

<style scoped>
.login-form {
    max-width: 400px;
    margin: 40px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
}
h2 {
    text-align: center;
}
.form-group {
    margin-bottom: 15px;
}
label {
    display: block;
    margin-bottom: 5px;
}
input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
}
button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
button:hover {
    background-color: #0056b3;
}
.error {
    color: red;
    text-align: center;
    margin-top: 10px;
}
</style>