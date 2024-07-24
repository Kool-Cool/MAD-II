<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
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
  methods: {
    async logout() {
      try {
        // Send a request to the backend to invalidate the token
        await axios.post('/logout');
        
        // Remove JWT from local storage
        localStorage.removeItem('jwt');
        
        // Redirect to the home or login page
        this.$router.push('/');
      } catch (error) {
        console.error("Logout failed:", error);
      }
    }
  }
};
</script>
