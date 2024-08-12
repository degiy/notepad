import { createRouter, createWebHistory } from 'vue-router'
import Notepad from '../views/Notepad.vue'
import Editor from '../views/Editor.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Notepad',
      component: Notepad
    },
    {
      path: '/editor',
      name: 'Editor',
      component: Editor
    }
  ]
})

export default router
