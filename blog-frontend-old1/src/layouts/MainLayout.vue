<template>
  <div class="main-layout">
    <!-- 顶部导航栏（全局共享） -->
    <el-menu mode="horizontal" default-active="home" class="nav-menu">
      <el-menu-item index="home" @click="$router.push('/')">首页</el-menu-item>
      <el-menu-item index="categories" @click="$router.push('/categories')">分类</el-menu-item>
      <el-menu-item index="about" @click="$router.push('/about')">关于我</el-menu-item>
      <!-- 可以添加管理员入口 -->
      <el-menu-item index="admin" @click="$router.push('/admin/articles')">管理</el-menu-item>
    </el-menu>

    <!-- 页面内容区域（动态渲染路由组件） -->
    <main class="content-container">
      <router-view />
    </main>

    <!-- 页脚（可选） -->
    <footer class="footer">
      <p>© 个人博客 - 基于Vue 3 + Element Plus构建</p>
    </footer>
  </div>
</template>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.nav-menu {
  margin-bottom: 0;
  border-radius: 0;
}

.content-container {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 20px;
}

.footer {
  text-align: center;
  padding: 20px;
  border-top: 1px solid var(--color-border);
  margin-top: 40px;
}
</style>