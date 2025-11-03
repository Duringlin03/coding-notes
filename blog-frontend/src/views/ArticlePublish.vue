<!-- src/views/ArticlePublish.vue -->
<template>
  <div class="publish-container">
    <div class="publish-content">
      <div class="publish-header">
        <h1>发布文章</h1>
        <p>分享你的想法和见解</p>
      </div>

      <form @submit.prevent="publishArticle" class="publish-form">
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
            :disabled="publishing"
          >
            取消
          </button>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="publishing || !isFormValid"
          >
            <span v-if="publishing" class="btn-loading"></span>
            {{ publishing ? '发布中...' : '发布文章' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/utils/request'

const router = useRouter()
const categories = ref([])
const publishing = ref(false)

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
    const res = await request.get('/categories')
    categories.value = res.data || []
  } catch (error) {
    console.error('获取分类失败:', error)
  }
})

const publishArticle = async () => {
  if (!isFormValid.value) return

  publishing.value = true
  try {
    const selectedCategory = categories.value.find(cat => cat.id == articleForm.value.categoryId)
    
    const articleData = {
      title: articleForm.value.title.trim(),
      content: articleForm.value.content.trim(),
      category: selectedCategory
    }

    const res = await request.post('/articles', articleData)
    
    // 发布成功，跳转到文章详情页
    router.push(`/article/${res.data.id}`)
  } catch (error) {
    console.error('发布文章失败:', error)
    alert('发布失败，请重试')
  } finally {
    publishing.value = false
  }
}

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.publish-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.publish-content {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.publish-header {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid #e2e8f0;
}

.publish-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 1rem;
}

.publish-header p {
  font-size: 1.125rem;
  color: #718096;
}

.publish-form {
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
  justify-content: flex-end;
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

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .publish-container {
    padding: 1rem;
  }
  
  .publish-content {
    padding: 2rem;
  }
  
  .publish-header h1 {
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
