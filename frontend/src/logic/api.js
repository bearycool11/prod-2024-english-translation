import axios from 'axios'
import { store } from '@/store/index.js'

class Api {
  constructor() {
    this.client = axios.create()

    this.client.interceptors.request.use(
      (config) => {
        if (!localStorage.getItem('token')) {
          return config
        }

        const newConfig = {
          headers: {},
          ...config
        }

        newConfig.headers.Authorization = `Bearer ${localStorage.getItem('token')}`
        return newConfig
      },
      (e) => Promise.reject(e)
    )

    this.client.interceptors.response.use(
      (r) => r,
      async (error) => {
        if (
          !localStorage.getItem('refreshToken') ||
          error.response.status !== 401 ||
          error.config.retry
        ) {
          store.auth.isAuth = false
          throw error
        }
      }
    )
  }

  async register({ login, password }) {
    await this.client.post(`${import.meta.env.VITE_BACKEND_URL}/auth/register`, {
      login,
      password,
      name: login
    })
    const { data } = await this.client.post(`${import.meta.env.VITE_BACKEND_URL}/auth/sign-in`, {
      login,
      password
    });

    localStorage.setItem('token', data.token)
    localStorage.setItem('refreshToken', data.refreshToken)
  }

  async login({ login, password }) {
    const { data } = await this.client.post(`${import.meta.env.VITE_BACKEND_URL}/auth/sign-in`, {
      login,
      password
    });

    localStorage.setItem('token', data.token)
    localStorage.setItem('refreshToken', data.refreshToken)
  }

  syncAuth() {
    return this.client.get(`${import.meta.env.VITE_BACKEND_URL}/organizations`)
  }

  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  }
}

export const api = new Api()
