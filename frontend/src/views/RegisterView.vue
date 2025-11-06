<template>
    <div>
        <h2>Register</h2>
        <form @submit.prevent="register">
            <input type="text" v-model="username" placeholder="Username" required>
            <input type="password" v-model="password" placeholder="Password" required>
            <button type="submit">Register</button>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const username = ref('');
const password = ref('');
const router = useRouter();

const register = async () => {
    try {
        await api.post('/users/register/', {
            username: username.value,
            password: password.value,
        });
        router.push('/login');
    } catch (error) {
        console.error(error);
    }
};
</script>
