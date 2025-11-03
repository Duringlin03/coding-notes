<template>
  <div class="about-container">
    <el-card>
      <div slot="header">
        <h1>关于博客</h1>
      </div>
      
      <div class="about-content">
        <h2>博主介绍</h2>
        <p>欢迎来到我的个人博客！我是一名开发者，热爱技术分享和记录生活点滴。</p>
        
        <h2>博客说明</h2>
        <p>本博客基于 Vue 3 + Element Plus 开发，用于分享技术文章、学习笔记和生活感悟。</p>
        
        <h2>联系方式</h2>
        <p>邮箱：example@mail.com</p>
        <p>GitHub：<a href="https://github.com" target="_blank">https://github.com</a></p>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AboutView'
}
</script>

<style scoped>
.about-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 20px;
}

.about-content {
  line-height: 1.8;
}

.about-content h2 {
  margin: 20px 0 10px;
  color: #333;
}

.about-content a {
  color: #409eff;
  text-decoration: none;
}

.about-content a:hover {
  text-decoration: underline;
}
</style>