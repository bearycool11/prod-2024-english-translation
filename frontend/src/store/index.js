import { reactive } from 'vue'

export const store = reactive({
  auth: {
    isAuth: false,
    isLoading: true,
    username: '',
    bot_id: 0,
    permissions: []
  },
  ui: {
    isSideBarOpen: false
  },
  data: {
    users: [],
    userModal: {},
    organizations: [],
    bots: [],
    canAddBots: false,
    channels: [],
    posts: []
  }
})
