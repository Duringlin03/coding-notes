<template>
    <nav class="blog-nav">
        <div class="nav-brand">
            <h1>Blog-parent</h1>
        </div>
        <div class="nav-links">
            <router-link to="/" class="nav-link">首页</router-link>
            <router-link to="/articles" class="nav-link">所有文章</router-link>
            <router-link to="/about" class="nav-link">关于</router-link>
        </div>
    </nav>
</template>

<script setup lang="ts">
// 这里可以添加组件逻辑
</script>

<style scoped>
.blog-nav {
    background: #2c3e50;
    color: white;
    width: 250px;
    height: 100vh;
    padding: 2rem 1rem;
    display: flex;
    flex-direction: column;
    position: fixed;
    left: 0;
    top: 0;
}

.nav-brand h1 {
    margin: 0 auto 2rem;
    font-size: 1.8rem;
    text-orientation: mixed;
}

.nav-links {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.nav-link {
    color: white;
    text-decoration: none;
    padding: 0.8rem 1rem;
    border-radius: 4px;
    transition: background-color 0.3s;
    text-align: center;
}

.nav-link:hover,
.nav-link.router-link-active {
    background-color: rgba(255, 255, 255, 0.1);
}
</style>