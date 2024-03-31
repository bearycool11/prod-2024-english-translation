import axios from 'axios'
import { useAuthStore } from './stores/auth'
import router from './router'

const axiosApiInstance = axios.create()

axiosApiInstance.interceptors.request.use((config) => {
  const url = config.url
  if (!url.includes('signInWithPassword') && !url.includes('signUp')) {
    const authStore = useAuthStore()
    let params = new URLSearchParams()
    params.append('auth', authStore.userInfo.token)
    config.params = params
  }
  return config
})

axiosApiInstance.interceptors.response.use(
  (response) => {
    return response
  },
  async function (error) {
    const authStore = useAuthStore()
    const originalRequest = error.config
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
        localStorage.removeItem('token')
        router.push('/login')
        authStore.userInfo.token = ''
      }
    }  
)

export default axiosApiInstance
