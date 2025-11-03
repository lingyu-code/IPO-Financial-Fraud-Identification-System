import './assets/main.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(ElementPlus, {
    locale: zhCn, // 正确的参数传递方式
})

app.use(createPinia())
app.use(router)

app.mount('#app')
