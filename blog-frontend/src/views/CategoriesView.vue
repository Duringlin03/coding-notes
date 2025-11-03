<!-- src/views/CategoriesView.vue -->
<template>
  <div class="categories-container">
    <div class="page-header">
      <h1>文章分类</h1>
      <p>按分类浏览所有文章</p>
    </div>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="categories.length" class="categories-grid">
      <div 
        v-for="category in categories" 
        :key="category.id" 
        class="category-card"
        @click="goToCategory(category.id)"
      >
        <div class="category-content">
          <h3 class="category-name">{{ category.name }}</h3>
          <p class="category-count">{{ getCategoryArticleCount(category.id) }} 篇文章</p>
          <p class="category-description">{{ getCategoryDescription(category.name) }}</p>
        </div>
        <div class="category-arrow">→</div>
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">📂</div>
      <h3>暂无分类</h3>
      <p>还没有创建任何分类。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/utils/request'

const router = useRouter()
const categories = ref([])
const articles = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [categoriesRes, articlesRes] = await Promise.all([
      request.get('/categories'),
      request.get('/articles')
    ])
    
    categories.value = categoriesRes.data || []
    articles.value = articlesRes.data || []
  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
})

const goToCategory = (categoryId) => {
  router.push(`/category/${categoryId}`)
}

const getCategoryArticleCount = (categoryId) => {
  return articles.value.filter(article => article.category?.id === categoryId).length
}

const getCategoryDescription = (categoryName) => {
  const descriptions = {
    '技术': '分享编程技术、开发经验和工具使用',
    '生活': '记录生活感悟、旅行见闻和日常思考',
    '学习': '学习笔记、读书心得和知识总结',
    '随笔': '随想随写，记录当下的想法和感受'
  }
  return descriptions[categoryName] || '暂无描述'
}
</script>

<style scoped>
.categories-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 1rem;
}

.page-header p {
  font-size: 1.125rem;
  color: #718096;
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

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.category-card {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  border-color: #667eea;
}

.category-content {
  flex: 1;
}

.category-name {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.category-count {
  color: #667eea;
  font-weight: 500;
  margin-bottom: 0.75rem;
}

.category-description {
  color: #718096;
  line-height: 1.6;
  font-size: 0.875rem;
}

.category-arrow {
  font-size: 1.5rem;
  color: #cbd5e0;
  transition: all 0.3s ease;
}

.category-card:hover .category-arrow {
  color: #667eea;
  transform: translateX(4px);
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

.empty-state h3 {
  color: #2d3748;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .categories-container {
    padding: 1rem;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .categories-grid {
    grid-template-columns: 1fr;
  }
  
  .category-card {
    padding: 1.5rem;
  }
}
</style>

