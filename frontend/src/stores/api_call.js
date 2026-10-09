import {reactive} from 'vue'
import axios from 'axios'

const API_BASE_URL = "http://127.0.0.1:8000/api"
export const apiCallStore = reactive({
    isLoading: false,
    error: null,
    data: null,
    async check_proxy(proxy_info, ...args) {
        // console.log("check_proxy called with:", proxy_info, args)
        this.isLoading = true
        this.error = null
        this.data = null
        try {
            const response = await axios.post(`${API_BASE_URL}/browsers/proxy-status`, { ...proxy_info, ...args })
            this.data = response.data
            return response
        } catch (error) {
            this.error = error.response?.data?.error || error.message || 'An error occurred'
            throw error
        } finally {
            this.isLoading = false
        }
    },
})