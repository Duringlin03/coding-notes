import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from './utils/axios'

const app = createApp(App)

// 全局注册Element Plus
app.use(ElementPlus)
app.use(router)

// 全局挂载axios
app.config.globalProperties.$axios = axios

app.mount('#app')
