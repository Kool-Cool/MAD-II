<script setup>
import Logout from "../Logout/performLogout.vue";
</script>

<template>
  <Logout DashboardTitle="Admin Dashboard"></Logout>
  <div class="dashboard container mt-5">
    <div v-if="stats" class="row">
      <div class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Total Users</h5>
            <p class="card-text">{{ stats.total_users }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Total Sponsors</h5>
            <p class="card-text">{{ stats.total_sponsors }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Public Campaigns</h5>
            <p class="card-text">{{ stats.total_campaigns_public }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Private Campaigns</h5>
            <p class="card-text">{{ stats.total_campaigns_private }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Pending Ad Requests</h5>
            <p class="card-text">{{ stats.total_ad_requests_pending }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card highlight">
          <div class="card-body">
            <h5 class="card-title">
              <a
                href="http://localhost:5173/admin/pending_sponsors"
                class="highlight-link"
                >Pending Sponsors Approval</a
              >
            </h5>
            <p class="card-text">{{ stats.pending_sponsors }}</p>
          </div>
        </div>
      </div>

      <!-- Add more statistics as needed -->
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      stats: null,
    };
  },
  async created() {
    try {
      const response = await axios.get(
        "http://localhost:5000/admin/dashboard/data",
        {
          headers: { Authorization: `Bearer ${this.$store.state.token}` },
        }
      );
      // console.log('Dashboard data:', response.data);
      this.stats = response.data;
    } catch (error) {
      console.error("Failed to fetch dashboard data:", error);
    }
  },
};
</script>

<style scoped>
.highlight {
  border: 2px solid blueviolet; /* Highlight border color */
}

.highlight-link {
  color: #ffcc00; /* Highlight link color */
  font-weight: bold;
}
</style>
