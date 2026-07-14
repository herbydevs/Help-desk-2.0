<template>  
    <div align="center">        
        <img src="../assets/cardtp.png" alt="cardtp logo" class="logo"  />
        <h2>Help Desk</h2>
    </div>
    <div class="login-form">
        
   
      
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
        <br/>
        <div>
        <RouterLink to="/register">Register</RouterLink></div>
        <div v-if="error" class="error">{{ error }}</div>
    </div>
</template>

<script>
import { ref ,nextTick} from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

export default {
    name: 'Login',
    setup(_, { emit }) {
        const email = ref('');
        const password = ref('');
        const error = ref('');
        const router = useRouter();
        const auth = useAuthStore();

        const handleLogin = async (event) => {
            event.preventDefault(); 
            try {
                const response = await fetch("/api/login", {
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
                //    localStorage.setItem('token', data.token);
                //   localStorage.setItem('user', JSON.stringify(data.user));
                    auth.setUser(data.user, data.token); // store both
                    emit('login-success', data.user); // Pass the user data including is_admin
                
                   if (data.user.admin) {
                    console.log("User Admin: "+data.user.admin)
                   // await nextTick();
                        router.push('/tickets');
                    } else {
                        router.push('/');
                    }
                } else {
                    error.value = data.detail ;
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
.logo {
  height: 80px;
}
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