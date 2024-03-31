import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './store/auth.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('./pages/MainLayout.vue'),
      meta: {
        auth: true
      },
      children: [
        {
          path: '/organization/:id',
          name: 'OrganizationPage',
          component: () => import('./pages/OrganizationLayout.vue'),
          meta: {
            auth: true
          },
          children: [
            {
              path: '/users',
              name: 'users'
            },
            {
              path: '/history',
              name: 'posts history'
            },
            {
              path: '/channels',
              name: 'channels'
            },
            {
              path: '/social',
              name: 'social networks'
            }
          ]
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('./pages/Login.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.auth && !authStore.userInfo.token) {
    next('/login')
  } else if (!to.meta.auth && authStore.userInfo.token) {
    next('/')
  } else {
    next();
  }
})

export default router

