<template>
  <div class="home-container">
    <!-- 页面标题 -->
    <h1>我的技术博客</h1>
    <p class="subtitle">分享编程知识与学习心得</p>

    <!-- 分类筛选区 -->
    <div class="category-filter">
      <button v-for="category in categories" :key="category.id" @click="selectCategory(category.id)"
        :class="{ active: selectedCategory === category.id }" class="category-btn">
        {{ category.name }}
      </button>
    </div>

    <!-- 文章列表 -->
    <div class="article-list">
      <div v-for="article in filteredArticles" :key="article.id" class="article-card" @click="viewArticle(article.id)">
        <h2 class="article-title">{{ article.title }}</h2>
        <div class="article-meta">
          <span class="category">{{ article.category?.name }}</span>
          <span class="views">阅读 {{ article.viewCount }}</span>
          <span class="date">{{ formatDate(article.createTime) }}</span>
        </div>
        <p class="article-excerpt">{{ getExcerpt(article.content) }}</p>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="!loading && filteredArticles.length === 0" class="no-data">
      暂无文章
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// 定义文章接口类型
interface Article {
  id: number
  title: string
  content: string
  viewCount: number
  createTime: string
  category?: {
    id: number
    name: string
  }
}

// 定义分类接口类型
interface Category {
  id: number
  name: string
}

const router = useRouter()
const articles = ref<Article[]>([])
const categories = ref<Category[]>([])
const selectedCategory = ref<number | null>(null)
const loading = ref(true)

// 模拟数据（后续替换为真实API调用）
const mockArticles: Article[] = [
  {
    id: 1,
    title: 'Vue 3 入门指南',
    content: '本文介绍Vue 3的基础用法和核心概念，帮助初学者快速上手...',
    viewCount: 156,
    createTime: '2024-01-15T10:30:00',
    category: { id: 1, name: '前端开发' }
  },
  {
    id: 2,
    title: 'Spring Boot 实战教程',
    content: '通过实际项目案例讲解Spring Boot的开发技巧和最佳实践...',
    viewCount: 89,
    createTime: '2024-01-10T14:20:00',
    category: { id: 2, name: '后端开发' }
  }
]

const mockCategories: Category[] = [
  { id: 1, name: '前端开发' },
  { id: 2, name: '后端开发' },
  { id: 3, name: '数据库' },
  { id: 4, name: 'DevOps' }
]

// 计算属性：根据选择分类过滤文章
const filteredArticles = computed(() => {
  if (!selectedCategory.value) {
    return articles.value
  }
  return articles.value.filter(article =>
    article.category?.id === selectedCategory.value
  )
})

// 选择分类
const selectCategory = (categoryId: number) => {
  selectedCategory.value = selectedCategory.value === categoryId ? null : categoryId
}

// 查看文章详情
const viewArticle = (id: number) => {
  router.push(`/article/${id}`)
}

// 格式化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 获取内容摘要
const getExcerpt = (content: string) => {
  return content.length > 100 ? content.substring(0, 100) + '...' : content
}

// 组件挂载时加载数据
onMounted(async () => {
  try {
    // 模拟网络请求延迟
    await new Promise(resolve => setTimeout(resolve, 1000))

    articles.value = mockArticles
    categories.value = mockCategories
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  margin-left: 250px;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 10px;
}

.subtitle {
  text-align: center;
  color: #7f8c8d;
  margin-bottom: 30px;
}

.category-filter {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.category-btn {
  padding: 8px 16px;
  border: 2px solid #3498db;
  background: white;
  color: #3498db;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.category-btn:hover {
  background: #3498db;
  color: white;
}

.category-btn.active {
  background: #3498db;
  color: white;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.article-card {
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: box-shadow 0.3s;
}

.article-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.article-title {
  color: #2c3e50;
  margin-bottom: 10px;
}

.article-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  font-size: 14px;
  color: #7f8c8d;
}

.article-meta span {
  display: flex;
  align-items: center;
}

.article-meta span::before {
  content: "•";
  margin-right: 5px;
}

.article-meta span:first-child::before {
  content: "";
  margin-right: 0;
}

.article-excerpt {
  color: #555;
  line-height: 1.6;
}

.loading,
.no-data {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}
</style>