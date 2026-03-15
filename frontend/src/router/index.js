import { createRouter, createWebHistory } from 'vue-router'
import FeedPage from '../pages/FeedPage.vue'

const routes = [
  { path: '/', component: FeedPage },
  { path: '/analysis/:postId?', component: FeedPage },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

export default createRouter({
  history: createWebHistory(),
  routes
})
