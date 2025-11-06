<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="login">
            <input type="text" v-model="username" placeholder="Username" required>
            <input type="password" v-model="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p v-if="loginError" class="error-message">{{ loginError }}</p>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { useAuthStore } from '@/stores/auth';

const username = ref('');
const password = ref('');
const loginError = ref('');
const router = useRouter();
const authStore = useAuthStore();

const login = async () => {
    try {
        const response = await api.post('/users/login/', {
            username: username.value,
            password: password.value,
        });
        authStore.login(response.data.token);
        router.push('/');
    } catch (error: any) {
        loginError.value = error.response?.data?.error || 'An unexpected error occurred.';
        console.error(error);
    }
};
</script>

<style scoped>
.error-message {
    color: red;
    margin-top: 10px;
}
</style>
