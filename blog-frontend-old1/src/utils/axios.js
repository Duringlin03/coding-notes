import axios from 'axios'

const instance = axios.create({
  baseURL: '/api', // 配合vue.config.js的代理配置
  timeout: 5000
})

// 请求拦截器（可添加token等）
instance.interceptors.request.use(
  config => {
    // 后续添加JWT认证：config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器（统一错误处理）
instance.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

export default instance