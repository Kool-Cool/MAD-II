import { createRouter, createWebHistory } from 'vue-router';
import IndexView from '@/views/IndexView.vue';
import NotFound from '@/views/NotFound/NotFound.vue';

const routes = [
  { path: '/', name: 'Home', component: IndexView },
  {path :'/:pathMatch(.*)*' ,name:'NotFound',component: NotFound},


];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
