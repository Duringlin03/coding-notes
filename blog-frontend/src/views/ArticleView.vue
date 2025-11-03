<!-- src/views/ArticleView.vue -->
<template>
  <div class="article-container">
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="article" class="article-content">
      <!-- Article Header -->
      <header class="article-header">
        <div class="article-meta">
          <span class="article-category">{{ article.category?.name || '未分类' }}</span>
          <span class="article-date">{{ formatDate(article.createTime) }}</span>
          <span class="article-views">{{ article.viewCount || 0 }} 阅读</span>
        </div>
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-actions">
          <button @click="goBack" class="back-btn">
            ← 返回
          </button>
          <button @click="editArticle" class="edit-btn">
            ✏️ 编辑
          </button>
        </div>
      </header>

      <!-- Article Body -->
      <div class="article-body">
        <div class="article-text" v-html="formatContent(article.content)"></div>
      </div>

      <!-- Article Footer -->
      <footer class="article-footer">
        <div class="article-tags">
          <span class="tag">#{{ article.category?.name || '未分类' }}</span>
        </div>
        <div class="article-share">
          <button @click="shareArticle" class="share-btn">分享</button>
        </div>
      </footer>
    </div>
    
    <div v-else class="error-state">
      <div class="error-icon">❌</div>
      <h3>文章不存在</h3>
      <p>抱歉，您访问的文章不存在或已被删除。</p>
      <button @click="goBack" class="back-btn">返回首页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '@/utils/request'

const route = useRoute()
const router = useRouter()
const article = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await request.get(`/articles/${route.params.id}`)
    article.value = res.data
    
    // 增加阅读量
    if (article.value) {
      await request.post(`/articles/${route.params.id}/view`)
    }
  } catch (error) {
    console.error('获取文章详情失败:', error)
    article.value = null
  } finally {
    loading.value = false
  }
})

const goBack = () => {
  router.go(-1)
}

const editArticle = () => {
  router.push(`/edit/${route.params.id}`)
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatContent = (content) => {
  if (!content) return ''
  // 简单的换行处理
  return content.replace(/\n/g, '<br>')
}

const shareArticle = () => {
  if (navigator.share) {
    navigator.share({
      title: article.value.title,
      text: `查看这篇文章：${article.value.title}`,
      url: window.location.href
    })
  } else {
    // 复制链接到剪贴板
    navigator.clipboard.writeText(window.location.href).then(() => {
      alert('链接已复制到剪贴板')
    })
  }
}
</script>

<style scoped>
.article-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  margin-top: 2rem;
  margin-bottom: 2rem;
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

.article-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #e2e8f0;
}

.article-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  color: #718096;
}

.article-category {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.article-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  line-height: 1.2;
  margin-bottom: 1rem;
}

.article-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.back-btn {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #4a5568;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.edit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.edit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.article-body {
  margin-bottom: 2rem;
}

.article-text {
  font-size: 1.125rem;
  line-height: 1.8;
  color: #2d3748;
}

.article-text :deep(h1),
.article-text :deep(h2),
.article-text :deep(h3) {
  color: #2d3748;
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.article-text :deep(p) {
  margin-bottom: 1.5rem;
}

.article-text :deep(ul),
.article-text :deep(ol) {
  margin-bottom: 1.5rem;
  padding-left: 2rem;
}

.article-text :deep(li) {
  margin-bottom: 0.5rem;
}

.article-text :deep(blockquote) {
  border-left: 4px solid #667eea;
  padding-left: 1rem;
  margin: 1.5rem 0;
  color: #4a5568;
  font-style: italic;
}

.article-text :deep(code) {
  background: #f8fafc;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.875rem;
}

.article-text :deep(pre) {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1.5rem 0;
}

.article-text :deep(pre code) {
  background: none;
  padding: 0;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1.5rem;
  border-top: 2px solid #e2e8f0;
}

.article-tags {
  display: flex;
  gap: 0.5rem;
}

.tag {
  background: #e2e8f0;
  color: #4a5568;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.share-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.share-btn:hover {
  background: #5a67d8;
}

.error-state {
  text-align: center;
  padding: 3rem;
  color: #718096;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-state h3 {
  color: #2d3748;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .article-container {
    margin: 1rem;
    padding: 1.5rem;
  }
  
  .article-title {
    font-size: 2rem;
  }
  
  .article-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .article-footer {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>