<template>
  <div class="article-edit">
    <el-form :model="articleForm" label-width="80px" @submit.prevent="saveArticle">
      <el-form-item label="标题" required>
        <el-input v-model="articleForm.title" style="width: 600px;"></el-input>
      </el-form-item>
      
      <el-form-item label="分类" required>
        <el-select v-model="articleForm.categoryId" style="width: 300px;">
          <el-option 
            v-for="category in categories" 
            :key="category.id" 
            :label="category.name" 
            :value="category.id"
          ></el-option>
        </el-select>
      </el-form-item>
      
      <el-form-item label="内容" required>
        <textarea 
          v-model="articleForm.content" 
          rows="20" 
          style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;"
        ></textarea>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" native-type="submit">保存</el-button>
        <el-button @click="$router.push('/admin/articles')">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from '@/utils/axios'
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'ArticleEdit',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const articleId = ref(route.query.id)
    const categories = ref([])
    const articleForm = ref({
      title: '',
      content: '',
      categoryId: ''
    })

    // 获取分类列表
    const fetchCategories = () => {
      axios.get('/categories').then(data => {
        categories.value = data
      })
    }

    // 获取文章详情（编辑模式）
    const fetchArticleDetail = () => {
      if (articleId.value) {
        axios.get(`/articles/${articleId.value}`).then(data => {
          articleForm.value = {
            title: data.title,
            content: data.content,
            categoryId: data.category.id
          }
        })
      }
    }

    // 保存文章（新增/编辑）
    const saveArticle = () => {
      if (articleId.value) {
        // 编辑模式
        axios.put(`/articles/${articleId.value}`, {
          ...articleForm.value,
          category: { id: articleForm.value.categoryId }
        }).then(() => {
          ElMessage.success('更新成功')
          router.push('/admin/articles')
        })
      } else {
        // 新增模式
        axios.post('/articles', {
          ...articleForm.value,
          category: { id: articleForm.value.categoryId }
        }).then(() => {
          ElMessage.success('创建成功')
          router.push('/admin/articles')
        })
      }
    }

    onMounted(() => {
      fetchCategories()
      fetchArticleDetail()
    })

    return {
      articleForm,
      categories,
      saveArticle
    }
  }
}
</script>