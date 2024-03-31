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
          name: 'OrganizationPage',
          //redirect: {name: 'posts'},
          children: [
            {
              path: '/',
              name: 'postsr',
              redirect: {name: 'posts'},
            },
            {
              path: '/posts',
              name: 'posts',
              component: () => import("./pages/TestPage.vue")
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
