import {onMounted, watch} from 'vue'
import { api } from '@/logic/api.js'
import router from "@/router.js";
import {store} from "@/store/index.js";

export const useAuth = () => {
  onMounted(async () => {
    store.auth.isLoading = true;
    await api.syncAuth()
      .catch(async () => {
        await router.push('/login');
      })
      .finally(() => {
        store.auth.isLoading = false;
      });
  });

  watch(store.auth, async (auth) => {
    console.log(store.auth);

    if (store.auth.isAuth && !store.auth.isLoading) {
      await router.push('/');
    } else if (!store.auth.isAuth && !store.auth.isLoading) {
      await router.push('/login');
    }
  });
}
