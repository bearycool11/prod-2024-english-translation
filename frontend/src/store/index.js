import { reactive } from 'vue'

export const store = reactive({
  auth: {
    isAuth: false,
    isLoading: true,
    username: '',
    bot_id: 0
  },
  ui: {
    isSideBarOpen: false
  },
  data: {
    organizations: [],
    bots: [],
    canAddBots: false,
    channels: []
  }
})
