<template>
  <div class="container">
    <h1>Message Component</h1>
    <p>This is the message: {{ message }}</p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const message = ref('');

    async function fetchData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/home');
        const data = await response.json();
        message.value = data.message;
      } catch (err) {
        console.error(err);
      }
    }

    onMounted(() => {
      fetchData();
    });

    return {
      message
    };
  }
};
</script>

<style scoped>
.container {
  text-align: center;
}
</style>
