import axios from 'axios'
import { store } from '@/store/index.js'
import { useToast } from 'vue-toast-notification'

import.meta.env.VITE_BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? '/api'

function compareISOStrings(a, b) {
  if (a > b) return -1
  if (a < b) return 1
  return 0
}
const $toast = useToast()

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
          $toast.error('Ошибка: что то пошло не так! повторите действие еще раз!')
          throw error
        }

        store.auth.isAuth = false
        throw error
      }
    )
  }

  async register({ login, password, name }) {
    await this.client.post(`${import.meta.env.VITE_BACKEND_URL}/auth/register`, {
      login,
      password,
      name
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

  getProfile() {
    return this.client.get(`${import.meta.env.VITE_BACKEND_URL}/auth/profile`).then(({ data }) => {
      return data.profile
    })
  }

  getOrganizationUsers(id) {
    return this.client
      .get(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/users`)
      .then(({ data }) => {
        if (data.reason) {
          return null
        }
        return data.users
      })
  }

  getOrganizationBots(id) {
    return this.client
      .get(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/bots`)
      .then(({ data }) => {
        if (data.reason) {
          return null
        }
        return data.bots
      })
  }
  deleteOrganizationBots(id, ch_id) {
    return this.client
      .delete(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/channels`, {
        data: { id: ch_id }
      })
      .then(({ data }) => {
        if (data.reason) {
          return null
        }
        return data.channels
      })
  }

  getUsers(id) {
    return this.client
      .get(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/users`)
      .then(({ data }) => {
        return data
      })
  }

  inviteUser(id, { permissions, login }) {
    return this.client
      .post(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/users`, { permissions, login })
      .then(({ data }) => {
        return data
      })
  }

  deleteUser(id, login) {
    return this.client
      .delete(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/users`, {
        data: {
          login
        }
      })
      .then(({ data }) => {
        return data
      })
  }

  updateUser(id, user) {
    return this.client
      .patch(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/users`, {
        ...user
      })
      .then(({ data }) => {
        return data
      })
  }

  createOrganizationBots(id, token) {
    return this.client
      .post(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/bots`, { token: token })
      .then(({ data }) => {
        if (data.reason) {
          throw 'Неверный токен'
        }
        return data.id
      })
      .catch(() => {
        throw 'Неправильный токен'
      })
  }

  getOrganizationInfo(id) {
    return this.client
      .get(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}`)
      .then(({ data }) => {
        if (data.reason) {
          return null
        }
        return data
      })
  }

  async addChannels(id, ch_id, bot_id, { chat_id, bot_token }) {
    const url = `https://api.telegram.org/bot${bot_token}/getChat?chat_id=${chat_id}`
   
    const data = await fetch(url)

    let json = await data.json()
    return this.client
      .post(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/channels`, {
        telegram_id: json.result.id,
        bot_id: bot_id
      })
      .then(({ data }) => {
        return data
      })
      .catch(() => {
        throw 'Канал не найден или уже используется'
      })
  }
  getChannels(id) {
    return this.client
      .get(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/channels`)
      .then(({ data }) => {
        if (data.reason) {
          return null
        }
        return data.channels
      })
  }

  deleteChannels(id, ch_id) {
    return this.client
      .delete(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/channels`, {
        data: { id: ch_id }
      })
      .then(({ data }) => {
        if (data.reason) {
          return null
        }
        return data.channels
      })
  }

  getPosts(id) {
    return this.client
      .get(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/posts`)
      .then(({ data }) => {
        if (data.reason) {
          return null
        }
        return [
          ...data.posts.sort((a, b) => compareISOStrings(a.update_time, b.update_time))
        ]
      })
  }
  getMyPermissions(id) {
    return this.client
      .get(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/mypermissions`)
      .then(({ data }) => {
        if (data.reason) {
          return null
        }
        return data.rights
      })
  }
  addPost(id, content, { channels }) {
    return this.client
      .post(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/posts`, {
        content: content,
        channels: channels
      })
      .then(({ data }) => {
        if (data.reason) {
          throw 'Вы не можете добавить пост'
        }
        return data
      })
      .catch(() => {
        throw 'Вы не можете добавить пост'
      })
  }

  getHistory(id) {
    return this.client
      .get(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/inactive_posts/`)
      .then(({ data }) => {
        if (data.reason) {
          throw 'Не удалось получить посты'
        }

        return [...data.posts.sort((a, b) => compareISOStrings(a.planned_time, b.planned_time))]
      })
      .catch(() => {
        throw 'Не удалось получить посты'
      })
  }

  schedulePost(id, time, post_id) {
    return this.client
      .post(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/posts/${post_id}/schedule`, {
        time: time
      })
      .then(({ data }) => {
        if (data.reason) {
          throw 'Не удалось отправить пост'
        }
        return data.rights
      })
      .catch(() => {
        throw 'Не удалось отправить пост'
      })
  }

  patchPost(
    id,
    post_id,
    { content = false, is_approved = false, comment = false, channels = false }
  ) {
    let data = { id: post_id }

    if (content) {
      data.content = content
    }
    if (is_approved) {
      data.is_approved = is_approved
    }
    if (comment) {
      data.comment = comment
    }
    if (channels) {
      data.channels = channels
    }

    return this.client
      .patch(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/posts`, data)
      .then(({ data }) => {
        if (data.reason) {
          throw 'Не удалось получить посты'
        }

        return data.posts
      })
      .catch(() => {
        throw 'Не удалось получить посты'
      })
  }

  addTagsToPost(id, post_id, tags) {
    return this.client
      .patch(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/posts`, { id: post_id, tags })
      .then(({ data }) => {
       
        if (data.reason) {
          throw 'Не удалось получить посты'
        }

        return data.posts
      })
      .catch(() => {
        throw 'Не удалось получить посты'
      })
  }

  deletePosts(id, post_id) {
    return this.client
      .delete(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/posts`, {
        data: { id: post_id }
      })
      .then(({ data }) => {
        return data
      })
      .catch(() => {
        throw 'Не удалось удалить'
      })
  }

  callEmergency(id) {
    return this.client
      .post(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/block_tasks`)
      .then(({ data }) => {
        return data
      })
      .catch(() => {
        throw 'Не работает кнопка'
      })
  }

  recallEmergency(id) {
    return this.client
      .post(`${import.meta.env.VITE_BACKEND_URL}/organizations/${id}/unblock_tasks`)
      .then(({ data }) => {
        return data
      })
      .catch(() => {
        throw 'Не работает кнопка'
      })
  }
}

export const api = new Api()
