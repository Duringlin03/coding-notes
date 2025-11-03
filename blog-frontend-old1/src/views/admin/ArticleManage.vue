<template>
  <div class="admin-container">
    <el-button type="primary" @click="$router.push('/admin/article-edit')">新增文章</el-button>
    
    <el-input 
      v-model="searchKeyword" 
      placeholder="搜索文章标题" 
      style="width: 300px; margin: 20px 0;"
      @keyup.enter="fetchArticles"
    ></el-input>

    <el-table :data="articles" border>
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="title" label="标题"></el-table-column>
      <el-table-column prop="category.name" label="分类"></el-table-column>
      <el-table-column prop="createTime" label="创建时间" :formatter="formatTime"></el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button type="text" @click="$router.push(`/admin/article-edit?id=${scope.row.id}`)">编辑</el-button>
          <el-button type="text" danger @click="deleteArticle(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from '@/utils/axios'
import { onMounted, ref } from 'vue'

export default {
  name: 'ArticleManage',
  setup() {
    const articles = ref([])
    const searchKeyword = ref('')

    const fetchArticles = () => {
      const url = searchKeyword.value 
        ? `/articles?keyword=${searchKeyword.value}` 
        : '/articles'
      axios.get(url).then(data => {
        articles.value = data
      })
    }

    const deleteArticle = (id) => {
      ElMessageBox.confirm('确定要删除这篇文章吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        axios.delete(`/articles/${id}`).then(() => {
          fetchArticles()
          ElMessage.success('删除成功')
        })
      })
    }

    const formatTime = (row) => {
      return new Date(row.createTime).toLocaleString()
    }

    onMounted(fetchArticles)

    return {
      articles,
      searchKeyword,
      fetchArticles,
      deleteArticle,
      formatTime
    }
  }
}
</script>