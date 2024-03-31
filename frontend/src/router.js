import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      children:[
        {
          path: '/organization/:id',
          name: 'organization page',
          children: [
            {
              path: '/',
              name: 'posts redirect',
              redirect: '/posts'
            },
            {
              path: '/posts',
              name: 'posts',
            },
            {
              path: '/users',
              name: 'users',
            },
            {
              path: '/history',
              name: 'posts history',
            },
            {
              path: '/channels',
              name: 'channels',
            },
            {
              path: '/social',
              name: 'social networks',
            }
          ]
        }
      ]
    }
  ]
})

export default router
