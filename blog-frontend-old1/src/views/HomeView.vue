<template>
  <div class="home-container">
    <!-- 顶部横幅区域（首页特有，保留） -->
    <div class="hero-banner">
      <h1>blog-parent</h1>
      <p>It's my blog</p>
    </div>

    <!-- 主体内容区：左侧文章列表 + 右侧边栏（首页核心内容，保留） -->
    <div class="main-content">
      <!-- 左侧内容区 -->
      <div class="article-list-wrapper">
        <!-- 分类筛选 -->
        <div class="category-filter">
          <el-select v-model="selectedCategoryId" placeholder="选择分类" @change="handleCategoryChange">
            <el-option label="全部文章" value=""></el-option>
            <el-option 
              v-for="category in categories" 
              :key="category.id" 
              :label="category.name" 
              :value="category.id"
            ></el-option>
          </el-select>
        </div>

        <!-- 文章列表 -->
        <el-card class="article-card" v-for="article in articles" :key="article.id">
          <div slot="header" class="article-header">
            <h2 @click="$router.push(`/article/${article.id}`)">{{ article.title }}</h2>
          </div>
          <div class="article-info">
            <span>分类: {{ article.category.name }}</span>
            <span>发布时间: {{ formatTime(article.createTime) }}</span>
          </div>
          <div class="article-content">
            {{ article.content.substring(0, 150) }}...
            <el-button type="text" @click="$router.push(`/article/${article.id}`)">阅读全文</el-button>
          </div>
        </el-card>

        <!-- 加载状态提示 -->
        <div v-if="articles.length === 0 && !loading" class="empty-tip">
          暂无文章数据，请先在后台添加文章
        </div>
        <el-loading v-if="loading" fullscreen></el-loading>
      </div>

      <!-- 右侧边栏（首页特有，保留） -->
      <div class="sidebar">
        <!-- 作者信息卡片 -->
        <el-card class="author-card">
          <div class="avatar">
            <img src="/avatar.jpg" alt="作者头像">
          </div>
          <h3>Blog of Lin</h3>
          <p>简介：分享生活与技术的个人博客</p>
        </el-card>

        <!-- 热门文章 -->
        <el-card class="hot-articles">
          <div slot="header">热门文章</div>
          <ul>
            <li v-for="article in hotArticles" :key="article.id">
              <a @click="$router.push(`/article/${article.id}`)">{{ article.title }}</a>
            </li>
          </ul>
        </el-card>

        <!-- 标签云 -->
        <el-card class="tag-cloud">
          <div slot="header">标签云</div>
          <div class="tags">
            <el-tag v-for="tag in tags" :key="tag.id" @click="filterByTag(tag.id)" effect="plain">
              {{ tag.name }}
            </el-tag>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios'
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus' // 引入ElMessage（保持错误提示功能）

export default {
  name: 'HomeView',
  setup() {
    const articles = ref([])
    const categories = ref([])
    const hotArticles = ref([])
    const tags = ref([])
    const selectedCategoryId = ref('')
    const loading = ref(true)

    // 获取所有文章（核心逻辑，保留）
    const fetchArticles = (categoryId = '', tagId = '') => {
      loading.value = true
      let url = '/articles'
      const params = []
      if (categoryId) params.push(`categoryId=${categoryId}`)
      if (tagId) params.push(`tagId=${tagId}`)
      if (params.length) url += `?${params.join('&')}`

      axios.get(url)
        .then(data => {
          articles.value = data
        })
        .catch(err => {
          console.error('获取文章失败:', err)
          ElMessage.error('获取文章列表失败，请稍后重试')
        })
        .finally(() => {
          loading.value = false
        })
    }

    // 获取所有分类（核心逻辑，保留）
    const fetchCategories = () => {
      axios.get('/categories')
        .then(data => {
          categories.value = data
        })
        .catch(err => {
          console.error('获取分类失败:', err)
          ElMessage.error('获取分类失败')
        })
    }

    // 获取热门文章（核心逻辑，保留）
    const fetchHotArticles = () => {
      axios.get('/articles/hot')
        .then(data => {
          hotArticles.value = data
        })
        .catch(err => console.error('获取热门文章失败:', err))
    }

    // 获取标签列表（核心逻辑，保留）
    const fetchTags = () => {
      axios.get('/tags')
        .then(data => {
          tags.value = data
        })
        .catch(err => console.error('获取标签失败:', err))
    }

    // 分类切换处理（核心逻辑，保留）
    const handleCategoryChange = (value) => {
      selectedCategoryId.value = value
      fetchArticles(value)
    }

    // 按标签筛选文章（核心逻辑，保留）
    const filterByTag = (tagId) => {
      fetchArticles('', tagId)
    }

    // 时间格式化（核心逻辑，保留）
    const formatTime = (time) => {
      return new Date(time).toLocaleString()
    }

    // 页面挂载时加载数据（核心逻辑，保留）
    onMounted(() => {
      fetchArticles()
      fetchCategories()
      fetchHotArticles()
      fetchTags()
    })

    return {
      articles,
      categories,
      hotArticles,
      tags,
      selectedCategoryId,
      handleCategoryChange,
      filterByTag,
      formatTime,
      loading
    }
  }
}
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 顶部横幅（首页特有样式，保留） */
.hero-banner {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  margin-bottom: 30px;
  border-radius: 8px;
}

.hero-banner h1 {
  font-size: 2.5rem;
  margin-bottom: 15px;
  color: #333;
}

.hero-banner p {
  font-size: 1.2rem;
  color: #666;
}

/* 主体内容布局（首页核心样式，保留） */
.main-content {
  display: flex;
  gap: 30px;
}

.article-list-wrapper {
  flex: 1;
}

.sidebar {
  width: 300px;
}

/* 分类筛选（首页特有样式，保留） */
.category-filter {
  margin: 20px 0;
  width: 200px;
}

/* 文章卡片（首页核心样式，保留） */
.article-card {
  margin-bottom: 20px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.article-header h2 {
  cursor: pointer;
  margin: 0;
}

.article-info {
  color: #666;
  margin: 10px 0;
  display: flex;
  gap: 20px;
}

.article-content {
  line-height: 1.6;
}

/* 空状态提示（首页特有样式，保留） */
.empty-tip {
  text-align: center;
  padding: 50px;
  color: #999;
}

/* 侧边栏组件（首页特有样式，保留） */
.author-card {
  text-align: center;
  padding: 20px 0;
  margin-bottom: 20px;
}

.avatar img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  margin: 0 auto 15px;
  object-fit: cover;
  border: 3px solid #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.hot-articles ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.hot-articles li {
  margin: 10px 0;
  padding-left: 10px;
  position: relative;
}

.hot-articles li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #409eff;
}

.hot-articles a {
  color: #333;
  text-decoration: none;
  transition: color 0.3s;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.hot-articles a:hover {
  color: #409eff;
}

.tag-cloud {
  margin-top: 20px;
}

.tag-cloud .tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-cloud .tags .el-tag {
  cursor: pointer;
  transition: all 0.2s;
}

.tag-cloud .tags .el-tag:hover {
  transform: scale(1.05);
}

/* 响应式调整（首页特有样式，保留） */
@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
  }
}
</style>