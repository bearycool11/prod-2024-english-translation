import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const userInfo = ref({
    token: '',
    email: '',
    userId: '',
  })
  const error = ref('');
  const loader = ref(false)

  const auth = async (payload, type) => {
    error.value = '';
    loader.value = true;
    try {
      let response = await axios.post(`http://84.201.175.97/api/auth/${type}`, {
        ...payload
      });
      userInfo.value = {
        token: response.data.token,
        email: response.data.email,
      }
      localStorage.setItem('token', JSON.stringify({
        token: userInfo.value.token}))
    } catch(err) {
      switch (err.response.data.error.message) {
        case 'EMAIL_EXISTS':
          error.value = 'Email exists'
          break;
        case 'OPERATION_NOT_ALLOWED':
          error.value = 'Operation not allowed'
          break;
        case 'EMAIL_NOT_FOUND':
          error.value = 'Email not found'
          break;
        case 'INVALID_PASSWORD':
          error.value = 'Invalid password'
          break;
        default:
          error.value = 'Error'
          break;
      }
      throw error.value;
    } finally {
      loader.value = false;
    }
  }

  const logout = () => {
    userInfo.value = {
      token: '',
      email: '',
      userId: '',
    }
  }

  return { auth, userInfo, error, loader, logout }
})