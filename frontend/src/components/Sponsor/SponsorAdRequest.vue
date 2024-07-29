<script setup>
import Logout from "@/views/Logout/Logout.vue";
import axios from "axios";


</script>

<template>
  <Logout DashboardTitle="Ad Requests"></Logout>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="ml-auto">
    <button class="btn btn-success mb-3" @click="navigateTo('add_adrequest')">
        + New AD request
      </button>
    </div>
  </nav>
  <div class="container mt-5">
    <h2 class="text-center mb-4">{{ campaign.name || "Campaign Details" }}</h2>
    <div v-if="messages.length" class="alert alert-danger">
      <ul>
        <li v-for="message in messages" :key="message">{{ message }}</li>
      </ul>
    </div>
    <div v-if="adRequests.length === 0" class="text-center">
      <p>No ad requests found for this campaign.</p>
    </div>
    <div v-else>
      <table class="table table-striped table-bordered">
        <thead>
          <tr>
            <th>Influencer</th>
            <th>Requirements</th>
            <th>Payment Amount</th>
            <th>Status</th>
            <th>Messages</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in adRequests" :key="request.ad_request_id">
            <td>{{ request.influencer.name }}</td>
            <td>{{ request.requirements }}</td>
            <td>{{ formatCurrency(request.payment_amount) }}</td>
            <td>{{ request.status }}</td>
            <td>{{ request.messages }}</td>
            <td>
              <button class="btn btn-primary btn-sm" @click="editAdRequest(request.ad_request_id)">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      adRequests: [],
      campaign: {},
      messages: [],
    };
  },
  created() {
    this.fetchAdRequests();
  },
  methods: {
    async fetchAdRequests() {
      const campaignId = this.$route.params.campaign_id;
      console.log("Cmap ID" , campaignId);
      const token = localStorage.getItem("token");

      if (!token) {
        this.messages = ["Authorization token is missing."];
        return;
      }

      try {
        

        const response = await axios.get(`/sponsor/adrequest_data/${campaignId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }}
        );

        if (response.status === 200) {

          // console.log(response.data)
          
          this.adRequests = response.data.adrequests;
          this.campaign = this.adRequests.length > 0 ? this.adRequests[0].campaign : {};
          this.messages = [];
        } else {
          this.messages = [response.data.message || "Error fetching data"];
        }
      } catch (error) {
  if (error.response) {
    // The request was made, and the server responded with a status code
    // that falls out of the range of 2xx
    this.messages.push({ message: error.response.data.message || "Error fetching data", type: "error" });
  } else if (error.request) {
    // The request was made but no response was received
    this.messages.push({ message: "No response received from server.", type: "error" });
  } else {
    // Something happened in setting up the request that triggered an Error
    this.messages.push({ message: "An error occurred: " + error.message, type: "error" });
  }
}
    },
    formatCurrency(amount) {
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
      }).format(amount);
    },
    navigateTo(route) {
      window.location.href = `/sponsor/${route}`;
    },
    editAdRequest(adRequestId) {
      // Navigate to the edit page with the ad request ID
      window.location.href = `/sponsor/edit_adrequest_data/${adRequestId}`;
    },
  },
};
</script>

<style scoped>
.table th, .table td {
  vertical-align: middle;
}
</style>
