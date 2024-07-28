import axios from 'axios';

// You can set a base URL for all requests
const API_BASE_URL = 'http://localhost:5000';

// export const fetchUserData = (token) => {
//   return axios.get(`${API_BASE_URL}/sponsor/profile`, {
//     headers: { Authorization: `Bearer ${token}` }
//   });
// };

// Add more functions for other API interactions
export const ApiCall = (token , api_route) => {
  return axios.post(`${API_BASE_URL}/${api_route}`, {
    headers : { Authorization: `Bearer ${token}` }
  });
};
