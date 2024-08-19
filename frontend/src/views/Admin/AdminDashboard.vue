<script setup>
import Logout from "../Logout/performLogout.vue";
import { ref, onMounted } from 'vue';
import axios from 'axios';

const stats = ref(null);
const admin = ref([]);
const influencer = ref([]);
const sponsor = ref([]);

const fetchStats = async () => {
  try {
    const response = await axios.get("http://localhost:5000/admin/dashboard/data", {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    });
    stats.value = response.data;
  } catch (error) {
    console.error("Failed to fetch dashboard data:", error);
  }
};

const fetchUsers = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/users');
    admin.value = response.data.admin;
    influencer.value = response.data.influencer;
    sponsor.value = response.data.sponsor;
  } catch (error) {
    console.error("Error while fetching users:", error);
  }
};

// Fetch data when component is mounted
onMounted(() => {
  fetchStats();
  fetchUsers();
});

// Define flagUser function
const flagUser = async (userId) => {
  const reason = prompt('Enter reason for flagging:');
  if (reason) {
    try {
      const response = await axios.post('http://localhost:5000/admin/flag_user', { user_id: userId, reason }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      alert('User flagged successfully!');
    } catch (error) {
      console.error('Error flagging user:', error);
      alert('Failed to flag user.');
    }
  }
};
</script>

<template>
  <Logout DashboardTitle="Admin Dashboard"></Logout>
  <div class="dashboard container mt-5">
    <div v-if="stats" class="row">
      <div class="col-md-4 mb-3" v-for="(value, key) in {
        'Total Users': stats.total_users,
        'Total Sponsors': stats.total_sponsors,
        'Public Campaigns': stats.total_campaigns_public,
        'Private Campaigns': stats.total_campaigns_private,
        'Pending Ad Requests': stats.total_ad_requests_pending ,
        'Flagged User' :  stats.flagged_users,
      }" :key="key">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ key }}</h5>
            <p class="card-text">{{ value }}</p>
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
              >Pending Sponsors Approval</a>
            </h5>
            <p class="card-text">{{ stats.pending_sponsors }}</p>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>

    <div>
      <h1>All Users</h1>
    </div>

    <h2>Admins</h2>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>User ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="adminItem in admin" :key="adminItem.user_id">
          <td>{{ adminItem.user_id }}</td>
          <td>{{ adminItem.username }}</td>
          <td>{{ adminItem.email }}</td>
          <td>{{ adminItem.created_at }}</td>
          <td>
            <button class="flag-button" @click="flagUser(adminItem.user_id)">Flag User</button>
          </td>
        </tr>
      </tbody>
    </table>

    <h2>Influencers</h2>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>User ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="influencerItem in influencer" :key="influencerItem.user_id">
          <td>{{ influencerItem.user_id }}</td>
          <td>{{ influencerItem.username }}</td>
          <td>{{ influencerItem.email }}</td>
          <td>{{ influencerItem.created_at }}</td>
          <td>
            <button class="flag-button" @click="flagUser(influencerItem.user_id)">Flag User</button>
          </td>
        </tr>
      </tbody>
    </table>

    <h2>Sponsors</h2>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>User ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sponsorItem in sponsor" :key="sponsorItem.user_id">
          <td>{{ sponsorItem.user_id }}</td>
          <td>{{ sponsorItem.username }}</td>
          <td>{{ sponsorItem.email }}</td>
          <td>{{ sponsorItem.created_at }}</td>
          <td>
            <button class="flag-button" @click="flagUser(sponsorItem.user_id)">Flag User</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.highlight {
  border: 2px solid blueviolet; /* Highlight border color */
}

.highlight-link {
  color: #ffcc00; /* Highlight link color */
  font-weight: bold;
}

.flag-button {
  background-color: #ff5722; /* Example color */
  color: #fff;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}
</style>
