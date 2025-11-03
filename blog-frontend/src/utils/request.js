import axios from 'axios'

const request = axios.create({
  baseURL: '/api', // 所有请求都会带上 /api 前缀，由代理转发
  timeout: 5000
})

export default request