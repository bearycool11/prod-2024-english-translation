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
          path: 'organization/:id',
          name: 'OrganizationPage',
          component: () => import('./pages/OrganizationLayout.vue'),
          props: true,
          meta: {
            auth: true
          },
          children: [
            {
              path: '',
              name: 'posts',
              props: true,
              component: () => import('./pages/PostsPage.vue')
            },
            {
              path: 'users',
              name: 'users',
              props: true,
              component: () => import('./pages/Users.vue')
            },
            {
              path: 'history',
              name: 'posts history',
              props: true,
              component: () => import('./pages/History.vue')
            },
            {
              path: 'post/:id',
              name: 'post stat',
              props: true,
              component: () => import('./pages/PostStat.vue')
            },
            {
              path: 'channels',
              name: 'channels',
              props: true,
              component: () => import('./pages/ChannelsPage.vue')
            },
            {
              path: 'social',
              name: 'social networks',
              props: true,
              component: () => import('./pages/SocialNetworks.vue')
            },
            {
              path: 'emergency',
              name: 'emergency',
              props: true,
              component: () => import('./pages/EmergencyButton.vue')
            }
          ]
        },
        {
          path: '',
          name: 'AllOrganization',
          component: () => import('./pages/AllOrganizations.vue')
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
