<!-- src/views/HomeView.vue -->
<template>
  <div class="home-container">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">欢迎来到我的博客</h1>
        <p class="hero-subtitle">分享技术见解，记录生活感悟</p>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-number">{{ articles.length }}</span>
            <span class="stat-label">篇文章</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ categories.length }}</span>
            <span class="stat-label">个分类</span>
          </div>
        </div>
        <div class="hero-actions">
          <router-link to="/publish" class="publish-btn">
            ✍️ 写文章
          </router-link>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <div class="main-container">
      <div class="content-wrapper">
        <!-- Articles Section -->
        <section class="articles-section">
          <div class="section-header">
            <h2>最新文章</h2>
            <router-link to="/categories" class="view-all-link">查看全部</router-link>
          </div>
          
          <div v-if="loading" class="loading">
            <div class="loading-spinner"></div>
            <p>加载中...</p>
          </div>
          
          <div v-else-if="articles.length" class="articles-grid">
            <article 
              v-for="article in articles.slice(0, 6)" 
              :key="article.id" 
              class="article-card"
              @click="goToArticle(article.id)"
            >
              <div class="article-content">
                <h3 class="article-title">{{ article.title }}</h3>
                <p class="article-excerpt">{{ getExcerpt(article.content) }}</p>
                <div class="article-meta">
                  <span class="article-category">{{ article.category?.name || '未分类' }}</span>
                  <span class="article-date">{{ formatDate(article.createTime) }}</span>
                  <span class="article-views">{{ article.viewCount || 0 }} 阅读</span>
                </div>
              </div>
            </article>
          </div>
          
          <div v-else class="empty-state">
            <div class="empty-icon">📝</div>
            <h3>暂无文章</h3>
            <p>还没有发布任何文章，请稍后再来查看。</p>
          </div>
        </section>

        <!-- Categories Section -->
        <aside class="categories-section">
          <h3>文章分类</h3>
          <div v-if="categories.length" class="categories-list">
            <router-link 
              v-for="category in categories" 
              :key="category.id" 
              :to="`/category/${category.id}`"
              class="category-item"
            >
              <span class="category-name">{{ category.name }}</span>
              <span class="category-count">{{ getCategoryArticleCount(category.id) }}</span>
            </router-link>
          </div>
          <div v-else class="empty-categories">
            <p>暂无分类</p>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/utils/request'

const router = useRouter()
const articles = ref([])
const categories = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [articlesRes, categoriesRes] = await Promise.all([
      request.get('/articles'),
      request.get('/categories')
    ])
    
    articles.value = articlesRes.data || []
    categories.value = categoriesRes.data || []
  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
})

const goToArticle = (id) => {
  router.push(`/article/${id}`)
}

const getExcerpt = (content, maxLength = 120) => {
  if (!content) return ''
  const plainText = content.replace(/<[^>]*>/g, '')
  return plainText.length > maxLength 
    ? plainText.substring(0, maxLength) + '...' 
    : plainText
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getCategoryArticleCount = (categoryId) => {
  return articles.value.filter(article => article.category?.id === categoryId).length
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
}

.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #fff, #e2e8f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin-top: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2.5rem;
  font-weight: 700;
  color: #fff;
}

.stat-label {
  font-size: 1rem;
  opacity: 0.8;
}

.hero-actions {
  margin-top: 2rem;
}

.publish-btn {
  display: inline-block;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 1rem 2rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.125rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.publish-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.content-wrapper {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 4rem;
}

.articles-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e2e8f0;
}

.section-header h2 {
  color: #2d3748;
  font-size: 1.5rem;
  font-weight: 600;
}

.view-all-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.view-all-link:hover {
  color: #5a67d8;
}

.loading {
  text-align: center;
  padding: 3rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.article-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  border-color: #667eea;
}

.article-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.article-excerpt {
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: #718096;
}

.article-category {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #718096;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.categories-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  height: fit-content;
}

.categories-section h3 {
  color: #2d3748;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #e2e8f0;
}

.categories-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #f8fafc;
  border-radius: 8px;
  text-decoration: none;
  color: #4a5568;
  transition: all 0.3s ease;
}

.category-item:hover {
  background: #667eea;
  color: white;
}

.category-name {
  font-weight: 500;
}

.category-count {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.category-item:hover .category-count {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.empty-categories {
  text-align: center;
  color: #718096;
  padding: 2rem;
}

@media (max-width: 1024px) {
  .content-wrapper {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .categories-section {
    order: -1;
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 2rem 1rem;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-stats {
    gap: 2rem;
  }
  
  .main-container {
    padding: 1rem;
  }
  
  .articles-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .article-card {
    padding: 1.5rem;
  }
}
</style>