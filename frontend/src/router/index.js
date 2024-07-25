import { createRouter, createWebHistory } from "vue-router";
import IndexView from "@/views/IndexView.vue";
import NotFound from "@/views/NotFound/NotFound.vue";
import AdminLogin from "@/views/Admin/AdminLogin.vue";
import AdminDashboard from "@/views/Admin/AdminDashboard.vue";
import AdminRegistration from "@/views/Admin/AdminRegistration.vue";
import AdminPendingSponsors from "@/views/Admin/AdminPendingSponsors.vue";
import SponsorLogin from "@/components/Sponsor/SponsorLogin.vue";
const routes = [
  { path: "/", name: "Home", component: IndexView },
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },

  //admin-path
  {
    path: "/admin/login",
    name: "AdminLogin",
    component: AdminLogin,
  },

  {
    path: "/admin/register",
    name: "AdminRegister",
    component: AdminRegistration,
  },
  {
    path: "/admin/dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/pending_sponsors",
    name: "AdninPendingSponsors",
    component: AdminPendingSponsors,
    meta: { requiresAuth: true },
  },

  //sponsor-paths

  {
    path: "/sponsor/login",
    name: SponsorLogin,
    component: SponsorLogin,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
