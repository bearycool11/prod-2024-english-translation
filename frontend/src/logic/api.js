import axios from 'axios'
import { store } from '@/store/index.js'

import.meta.env.VITE_BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? '/api'

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
        if (error.response.status !== 401) {
          throw error
        }

        store.auth.isAuth = false
        throw error
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
    })

    localStorage.setItem('token', data.token)
  }

  async login({ login, password }) {
    const { data } = await this.client.post(`${import.meta.env.VITE_BACKEND_URL}/auth/sign-in`, {
      login,
      password
    })

    localStorage.setItem('token', data.token)
  }

  createOrganization({ name, description }) {
    return this.client
      .post(`${import.meta.env.VITE_BACKEND_URL}/organizations`, {
        name,
        description
      })
      .then(({ data }) => {
        return data.organization
      })
  }

  getOrganizations() {
    return this.client.get(`${import.meta.env.VITE_BACKEND_URL}/organizations`).then(({ data }) => {
      return data.organizations
    })
  }

  async syncAuth() {
    return await this.client.get(`${import.meta.env.VITE_BACKEND_URL}/auth/check`)
  }
}

export const api = new Api()
