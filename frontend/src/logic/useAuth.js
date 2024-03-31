import { onMounted, watch } from 'vue'
import { api } from '@/logic/api.js'
import router from '@/router.js'
import { store } from '@/store/index.js'

export const useAuth = () => {
  onMounted(async () => {
    store.auth.isLoading = true
    await api
      .syncAuth()
      .then(() => {
        store.auth.isAuth = true
      })
      .catch(() => {
        store.auth.isAuth = false
      })
      .finally(() => {
        store.auth.isLoading = false
      })
  })

  watch(store.auth, async () => {
    if (!store.auth.isAuth && !store.auth.isLoading) {
      await router.push('/login')
    }
  })
}
