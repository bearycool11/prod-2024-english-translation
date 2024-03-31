import { reactive } from 'vue'

export const store = reactive({
  auth: {
    isAuth: false,
    isLoading: true
  },
  ui: {
    isSideBarOpen: false
  }
})
