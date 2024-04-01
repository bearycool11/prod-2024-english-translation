import { createRouter, createWebHistory } from 'vue-router'

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
          path: '/',
          name: 'AllOrganization',
          component: () => import('./pages/AllOrganizations.vue')
        },
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

export default router
