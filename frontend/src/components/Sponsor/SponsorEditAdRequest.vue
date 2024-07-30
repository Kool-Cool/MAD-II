<script setup>
import Logout from '@/views/Logout/Logout.vue';
</script>

<template>
    <Logout DashboardTitle="Edit Ad Request"></Logout>
    <div class="container">
        /sponsor/edit_adrequest_data/2
        ad_request_id
    </div>

    <div class="form-group">
          <label for="campaignname">Campaign Name:</label>
          <!-- <input type="text" v-model="ad_reqst.campaign_name" class="form-control" id="campaignname" required /> -->
           <p>{{ ad_reqst.campaign_name }}</p>
           <p>asdfsf</p>
    </div>

</template>

<script>
import axios from 'axios';

export default {
    data(){
        return{
            ad_reqst :{
                campaign_id : "",
                campaign_name : "",
                influencer_id : "",
                influencer_name : "",
                requirements : "",
                payment_amount : "",
                status : "",
                message :"",
            },
            messages: [],
            successMessage: '',
        };
    },
    created(){
        this.fetchAdReqstData();
    },
    methods : {
        async fetchAdReqstData() {
            const ad_request_id = this.$route.params.ad_request_id;
            const token = localStorage.getItem('token');
           
            try {
                const response = await axios.get(`/api/adrequest/${ad_request_id}`);
                this.ad_reqst = response.data;
                this.ad_reqst.campaign_name = (await axios.get(`/api/campaign/${this.ad_reqst.campaign_id}`)).data.name;
                this.ad_reqst.influencer_name = (await axios.get(`/api/influencer/${this.ad_reqst.influencer_id}`)).data.name;
            } catch (error) {
                console.error("Error fetching campaign data:", error);
                this.messages.push("An error occurred while fetching campaign data.");
            }
        },
    }
}
</script>
