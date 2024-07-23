<template>
    <div>
      Message components
      <br>
      This is message: {{ message }}
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    setup() {
      const message = ref('');
  
      async function fetchData() {
        try {
          const response = await fetch('http://127.0.0.1:5000/home');
          const data = await response.json();
          message.value = data.message;
        } catch (err) {
          console.log(err);
        }
      }
  
      fetchData();
      return {
        message,
      };
    },
  };
  </script>
  
  <style scoped>
  .container {
    text-align: center;
  }
  </style>
  