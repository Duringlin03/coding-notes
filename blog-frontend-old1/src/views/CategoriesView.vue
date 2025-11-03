<template>
  <div class="categories-container">
    <el-card>
      <div slot="header">
        <h1>文章分类</h1>
      </div>
      
      <div class="categories-list">
        <el-card 
          v-for="category in categories" 
          :key="category.id" 
          class="category-item"
        >
          <div class="category-name">
            <el-button 
              type="text" 
              @click="$router.push(`/?categoryId=${category.id}`)"
            >
              {{ category.name }}
            </el-button>
          </div>
          <div class="category-count">
            包含 {{ category.articleCount }} 篇文章
          </div>
        </el-card>
      </div>
      
      <div v-if="categories.length === 0" class="empty-tip">
        暂无分类数据
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from '@/utils/axios'
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'CategoriesView',
  setup() {
    const categories = ref([])

    // 获取所有分类及文章数量
    const fetchCategories = () => {
      axios.get('/categories?withCount=true')
        .then(data => {
          categories.value = data
        })
        .catch(err => {
          console.error('获取分类失败:', err)
          // 注意：需要先在main.js中全局注册ElMessage
          ElMessage.error('获取分类列表失败')
        })
    }

    onMounted(fetchCategories)

    return {
      categories
    }
  }
}
</script>

<style scoped>
.categories-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 20px;
}

.categories-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.category-item {
  text-align: center;
  padding: 20px 0;
  cursor: pointer;
  transition: transform 0.3s;
}

.category-item:hover {
  transform: translateY(-5px);
}

.category-name {
  font-size: 18px;
  margin-bottom: 10px;
}

.category-count {
  color: #666;
  font-size: 14px;
}

.empty-tip {
  text-align: center;
  padding: 50px;
  color: #999;
}
</style>