import { store } from '@/store/index.js'

export { store } from './index'

export const toggleSidebar = () => {
  store.ui.isSideBarOpen = !store.ui.isSideBarOpen
}
