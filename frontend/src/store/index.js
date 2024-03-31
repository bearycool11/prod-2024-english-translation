import {reactive} from "vue";

export const store = reactive({
  auth: {
    isAuth: false
  },
  ui: {
    isSideBarOpen: false
  }
});
