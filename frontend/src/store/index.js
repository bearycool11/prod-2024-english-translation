import { reactive } from 'vue'

export const store = reactive({
  auth: {
    isAuth: false,
    isLoading: true,
    username: ''
  },
  ui: {
    isSideBarOpen: false
  },
  data: {
    organizations: [],
    bots: [],
    canAddBots: false
  }
})
