import { createRouter, createWebHistory } from 'vue-router';
import IndexView from '@/views/IndexView.vue';
import NotFound from '@/views/NotFound/NotFound.vue';
import AdminLogin from '@/views/Admin/AdminLogin.vue';
import AdminDashboard from '@/views/Admin/AdminDashboard.vue';
import AdminRegistration from '@/views/Admin/AdminRegistration.vue';
import AdminPendingSponsors from '@/views/Admin/AdminPendingSponsors.vue';
const routes = [
  { path: '/', name: 'Home', component: IndexView },
  {path :'/:pathMatch(.*)*' ,name:'NotFound',component: NotFound},
  {
    path: '/admin/login',
    name: 'Login',
    component: AdminLogin,
  },

  {
    path: '/admin/register',
    name: 'Register',
    component: AdminRegistration,
  },
  {
    path: '/admin/dashboard',
    name: 'Dashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true },
  },
  {
    path:'/admin/pending_sponsors',
    name: 'pending_sponsors',
    component : AdminPendingSponsors,
    meta: { requiresAuth: true },
  }


];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
