<script setup>
import Logout from "@/views/Logout/Logout.vue";
import axios from "axios";

</script>
<template>
    <div>
        <Logout DashboardTitle="Edit Ad Request"></Logout>
        <div class="container">
            <!-- Displaying the ad request ID for reference -->
            <p>/sponsor/edit_adrequest_data/2</p>
            <p>{{ ad_request_id }}</p>
        </div>

        <div class="form-group">
            <label for="campaignname">Campaign Name:</label>
            <p>{{ ad_reqst.campaign_name }}</p>
            <p>asdfsf</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import Logout from '@/views/Logout/Logout.vue';

export default {
    components: {
        Logout,
    },
    data() {
        return {
            ad_reqst: {
                campaign_id: "",
                campaign_name: "",
                influencer_id: "",
                influencer_name: "",
                requirements: "",
                payment_amount: "",
                status: "",
                message: "",
            },
            messages: [],
            successMessage: '',
            ad_request_id: this.$route.params.ad_request_id,
        };
    },
    created() {
        this.fetchAdReqstData();
    },
    methods: {
    async fetchAdReqstData() {
        const ad_request_id = this.$route.params.ad_request_id;
        const token = localStorage.getItem('token');

        try {
            console.log(`Fetching ad request data for ID: ${ad_request_id}`);
            const response = await axios.get(`/api/adrequest/${ad_request_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                },
                timeout: 10000 // 10 seconds timeout
            });
            this.ad_reqst = response.data;
            console.log("Ad request data fetched:", this.ad_reqst);

            // Fetching additional data
            const campaignResponse = await axios.get(`/api/campaign/${this.ad_reqst.campaign_id}`);
            this.ad_reqst.campaign_name = campaignResponse.data.name;
            console.log("Campaign data fetched:", campaignResponse.data);

            const influencerResponse = await axios.get(`/api/influencer/${this.ad_reqst.influencer_id}`);
            this.ad_reqst.influencer_name = influencerResponse.data.name;
            console.log("Influencer data fetched:", influencerResponse.data);

        } catch (error) {
            console.error("Error fetching ad request data:", error);

            if (error.response) {
                console.error("Response data:", error.response.data);
                console.error("Response status:", error.response.status);
                console.error("Response headers:", error.response.headers);
            } else if (error.request) {
                console.error("Request data:", error.request);
            } else {
                console.error("Error message:", error.message);
            }

            this.messages.push("An error occurred while fetching ad request data.");
        }
    },
},

};
</script>

<style scoped>
/* Add your styles here */
</style>
