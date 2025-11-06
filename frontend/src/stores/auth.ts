import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', () => {
    const isAuthenticated = ref(!!localStorage.getItem('token'));

    function login(token: string) {
        localStorage.setItem('token', token);
        isAuthenticated.value = true;
    }

    function logout() {
        localStorage.removeItem('token');
        isAuthenticated.value = false;
    }

    return { isAuthenticated, login, logout };
});
