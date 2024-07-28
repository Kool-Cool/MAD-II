<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <a class="navbar-brand" href="#">{{ DashboardTitle }}</a>
      <ul class="navbar-nav ml-auto">
        <li class="nav-item">
          <button class="btn btn-outline-light" @click="logout">Logout</button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    DashboardTitle: {
      type: String,
      required: true
    }
  },
  methods: {
    async logout() {
      try {
        // Send a request to the backend to invalidate the token
        await axios.post('/logout');
        
        // Remove JWT from local storage
        localStorage.removeItem('token');
        
        // Redirect to the home or login page
        this.$router.push('/');
      } catch (error) {
        console.error("Logout failed:", error);
      }
    }
  }
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
