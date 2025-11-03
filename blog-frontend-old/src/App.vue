<script setup lang="ts">
import { RouterView } from 'vue-router'
import BlogNav from './components/BlogNav.vue' // 导入导航组件
</script>

<template>
  <div id="app">
    <BlogNav /> <!-- 使用导航组件 -->
    <RouterView />
  </div>
</template>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #f8f9fa;
  color: #2c3e50;
  line-height: 1.6;
}

#app {
  min-height: 100vh;
  display: flex;
  /* 使用flex布局实现左右结构 */
}

/* 确保 Vue 默认布局完全隐藏 */
header {
  display: none !important;
}

.wrapper {
  display: none !important;
}
</style>