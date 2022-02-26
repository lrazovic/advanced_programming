import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import store from './store'
import { darkModeKey } from '@/config.js'
import { SnackbarService, Vue3Snackbar } from "vue3-snackbar";
import "vue3-snackbar/dist/style.css";

import './css/main.css'
import Auth from "./packages/auth/auth";

/* Fetch sample data */


/* Dark mode */
const localStorageDarkModeValue = localStorage.getItem(darkModeKey)

if ((localStorageDarkModeValue === null && window.matchMedia('(prefers-color-scheme: dark)').matches) || localStorageDarkModeValue === '1') {
  store.dispatch('darkMode')
}

/* Default title tag */
const defaultDocumentTitle = 'Summary News Feed'

/* Collapse mobile aside menu on route change */
router.beforeEach((to) => {
  store.dispatch('asideMobileToggle', false)
  store.dispatch('asideLgToggle', false)

  if (to.meta.forAuth){
    if(!app.auth.isAuthenticated()) {
      router.push('/login')
    }
  }else if (to.meta.forVisitors) {
    if(app.auth.isAuthenticated()) {
      router.push('/')
    }
  }
})

router.afterEach(to => {
  /* Set document title from route meta */
  if (to.meta && to.meta.title) {
    document.title = `${to.meta.title} — ${defaultDocumentTitle}`
  } else {
    document.title = defaultDocumentTitle
  }

  /* Full screen mode */
  store.dispatch('fullScreenToggle', !!to.meta.fullScreen)
})


const app = createApp(App).use(store).use(router).use(Auth).use(SnackbarService)
app.component("vue3-snackbar", Vue3Snackbar);
app.mount('#app')
