import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('./pages/MainLayout.vue'),
      children: [
        {
          path: '/organization/:id',
          name: 'OrganizationPage',
          component: () => import('./pages/OrganizationLayout.vue'),
          //redirect: {name: 'posts'},
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
    }
  ]
})

export default router
