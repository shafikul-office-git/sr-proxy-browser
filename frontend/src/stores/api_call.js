import {reactive} from 'vue'
import axios from 'axios'

const API_BASE_URL = "http://127.0.0.1:8000/api"
export const apiCallStore = reactive({
    isLoading: false,
    error: null,
    data: null,
    format_error (collect_error){
        if (Array.isArray(collect_error)) {
            this.error = collect_error
                .map(item => {
                    const field = item.loc?.at(-1);
                    const msg = item.msg?.replace(/^Value error, /, '');

                    return field
                        ? `${field}: ${msg}`
                        : msg || 'Validation error';
                })
                .join('\n');
        } else if (typeof collect_error === 'string') {
            this.error = collect_error;
        } else {
            this.error = 'Proxy check failed';
        }
        return this.error
    },
    async check_proxy(proxy_info, ...args) {
        // console.log("check_proxy called with:", proxy_info, args)
        this.isLoading = true
        this.error = null
        this.data = null
        try {
            const response = await axios.post(`${API_BASE_URL}/proxy/status`, { ...proxy_info, ...args, protocol: proxy_info.protocol.toLowerCase() })
            this.data = response.data
            return response
        } catch (error) {
            const api_error = error.response?.data?.detail || error.response?.data?.error || error.message || 'An error occurred'
            return this.format_error(api_error)
        } finally {
            this.isLoading = false
        }
    },

    // sent browser profile data
    async create_browser_profile(profile_data) {
        this.isLoading = true
        this.error = null
        this.data = null
        try {
            const response = await axios.post(`${API_BASE_URL}/browser/add/profile`, profile_data)
            this.data = response.data
            return response
        }
        catch (error) {
            this.error = error.response?.data?.error || error.response?.data?.detail || error.message || 'An error occurred'
            return this.format_error(api_error)
        }
        finally {
            this.isLoading = false
        }
    }
})