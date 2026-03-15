import { createRouter, createWebHistory } from 'vue-router'
import FeedPage from '../pages/FeedPage.vue'

const routes = [
  { path: '/', name: 'feed', component: FeedPage },
  { path: '/analysis/:postId?', name: 'analysis', component: FeedPage },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})
