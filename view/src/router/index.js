import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    // Document title tag
    // We combine it with defaultDocumentTitle set in `src/main.js` on router.afterEach hook
    meta: {
      title: 'Feed',
      forAuth: true
    },
    path: '/',
    name: 'feed',
    component: () => import('@/views/NewsFeed.vue')
  },
  {
    meta: {
      title: 'Profile',
      forAuth: true
    },
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/Profile.vue')
  },
  {
    meta: {
      title: 'News Sources',
      forAuth: true
    },
    path: '/source-list',
    name: 'sources',
    component: () => import('@/views/SourceList.vue')
  },
  {
    meta: {
      title: 'Login',
      fullScreen: true,
      forVisitors: true
    },
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    meta: {
      title: 'Register',
      fullScreen: true,
      forVisitors: true
    },
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

export default router
