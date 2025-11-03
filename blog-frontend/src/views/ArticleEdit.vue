<!-- src/views/ArticleEdit.vue -->
<template>
  <div class="edit-container">
    <div class="edit-content">
      <div class="edit-header">
        <h1>编辑文章</h1>
        <p>修改你的文章内容</p>
      </div>

      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <form v-else-if="article" @submit.prevent="updateArticle" class="edit-form">
        <div class="form-group">
          <label for="title" class="form-label">文章标题 *</label>
          <input
            id="title"
            v-model="articleForm.title"
            type="text"
            class="form-input"
            placeholder="请输入文章标题"
            required
          />
        </div>

        <div class="form-group">
          <label for="category" class="form-label">文章分类 *</label>
          <select
            id="category"
            v-model="articleForm.categoryId"
            class="form-select"
            required
          >
            <option value="">请选择分类</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="content" class="form-label">文章内容 *</label>
          <textarea
            id="content"
            v-model="articleForm.content"
            class="form-textarea"
            placeholder="请输入文章内容..."
            rows="15"
            required
          ></textarea>
          <div class="char-count">{{ articleForm.content.length }} 字符</div>
        </div>

        <div class="form-actions">
          <button
            type="button"
            @click="goBack"
            class="btn btn-secondary"
            :disabled="updating"
          >
            取消
          </button>
          <button
            type="button"
            @click="deleteArticle"
            class="btn btn-danger"
            :disabled="updating"
          >
            删除文章
          </button>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="updating || !isFormValid"
          >
            <span v-if="updating" class="btn-loading"></span>
            {{ updating ? '更新中...' : '更新文章' }}
          </button>
        </div>
      </form>

      <div v-else class="error-state">
        <div class="error-icon">❌</div>
        <h3>文章不存在</h3>
        <p>抱歉，您要编辑的文章不存在或已被删除。</p>
        <button @click="goBack" class="btn btn-primary">返回首页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '@/utils/request'

const route = useRoute()
const router = useRouter()
const article = ref(null)
const categories = ref([])
const loading = ref(true)
const updating = ref(false)

const articleForm = ref({
  title: '',
  content: '',
  categoryId: ''
})

const isFormValid = computed(() => {
  return articleForm.value.title.trim() && 
         articleForm.value.content.trim() && 
         articleForm.value.categoryId
})

onMounted(async () => {
  try {
    const [articleRes, categoriesRes] = await Promise.all([
      request.get(`/articles/${route.params.id}`),
      request.get('/categories')
    ])
    
    article.value = articleRes.data
    categories.value = categoriesRes.data || []
    
    // 填充表单数据
    if (article.value) {
      articleForm.value = {
        title: article.value.title,
        content: article.value.content,
        categoryId: article.value.category?.id || ''
      }
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    article.value = null
  } finally {
    loading.value = false
  }
})

const updateArticle = async () => {
  if (!isFormValid.value) return

  updating.value = true
  try {
    const selectedCategory = categories.value.find(cat => cat.id == articleForm.value.categoryId)
    
    const articleData = {
      title: articleForm.value.title.trim(),
      content: articleForm.value.content.trim(),
      category: selectedCategory
    }

    await request.put(`/articles/${route.params.id}`, articleData)
    
    // 更新成功，跳转到文章详情页
    router.push(`/article/${route.params.id}`)
  } catch (error) {
    console.error('更新文章失败:', error)
    alert('更新失败，请重试')
  } finally {
    updating.value = false
  }
}

const deleteArticle = async () => {
  if (!confirm('确定要删除这篇文章吗？此操作不可撤销。')) return

  updating.value = true
  try {
    await request.delete(`/articles/${route.params.id}`)
    
    // 删除成功，跳转到首页
    router.push('/')
  } catch (error) {
    console.error('删除文章失败:', error)
    alert('删除失败，请重试')
  } finally {
    updating.value = false
  }
}

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.edit-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.edit-content {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.edit-header {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid #e2e8f0;
}

.edit-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 1rem;
}

.edit-header p {
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

.edit-form {
  max-width: 800px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 2rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 300px;
  font-family: inherit;
  line-height: 1.6;
}

.char-count {
  text-align: right;
  font-size: 0.875rem;
  color: #718096;
  margin-top: 0.5rem;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 2px solid #e2e8f0;
}

.btn {
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f8fafc;
  color: #4a5568;
  border: 2px solid #e2e8f0;
}

.btn-secondary:hover:not(:disabled) {
  background: #e2e8f0;
  border-color: #cbd5e0;
}

.btn-danger {
  background: #e53e3e;
  color: white;
  box-shadow: 0 2px 8px rgba(229, 62, 62, 0.3);
}

.btn-danger:hover:not(:disabled) {
  background: #c53030;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(229, 62, 62, 0.4);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-loading {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
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
  .edit-container {
    padding: 1rem;
  }
  
  .edit-content {
    padding: 2rem;
  }
  
  .edit-header h1 {
    font-size: 2rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
