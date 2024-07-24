<template>
  <div>
    <div id="navbar">
      <a class="navbar-brand" href="/admin/login"><button class="btn btn-primary">Admin Login Only</button></a>
    </div>

    <div id="flash" v-if="messages && messages.length > 0">
      <div class="alert alert-danger">
        <ul>
          <li v-for="message in messages" :key="message">{{ message }}</li>
        </ul>
      </div>
    </div>

    <div class="body-content">
      <div id="button_body">
        <h1><strong>Influencer Engagement and Sponsorship Coordination Platform</strong></h1>
        <h1>Choose Your Role</h1>
        <div class="button">
          <button class="btn btn-primary" @click="goTo('/sponsor/login')">Sponsor</button>
          <button class="btn btn-primary" @click="goTo('/influencer/login')">Influencer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Index',
  data() {
    return {
      messages: [] // Assuming you will pass messages as props or fetch them from a store/state
    };
  },
  methods: {
    goTo(path) {
      // Function to navigate to a specific path
      this.$router.push(path);
    },
    goToInfluencerLogin() {
      // Using Vue Router's $router.push with named route
      this.$router.push({ name: 'influencer.login' });
    }
  }
};
</script>

<style scoped>
.body-content {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  height: 100vh;
  background-color: #f8f9fa;
  font-family: 'Arial', sans-serif;
}

#navbar {
  width: 100%;
  padding: 10px;
  background-color: #343a40;
  color: white;
  text-align: center;
}

#navbar button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  margin: 5px;
  cursor: pointer;
  border-radius: 5px;
}

#flash {
  width: 100%;
  padding: 10px;
  text-align: center;
}

#button_body {
  text-align: center;
}

#button_body h1 {
  margin-bottom: 30px;
}

.button button {
  background-color: #007bff;
  color: white;
  border: none;
  height: 200px;
  width: 300px;
  padding: 15px 30px;
  margin: 10px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 40px;
  font-weight: 400;
}

.alert-danger {
  color: #721c24;
  background-color: #f8d7da;
  border-color: #f5c6cb;
  padding: 10px;
  border-radius: 5px;
}
</style>
