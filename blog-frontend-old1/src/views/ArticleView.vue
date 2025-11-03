<template>
  <div class="article-detail">
    <el-card>
      <div slot="header">
        <h1>{{ article.title }}</h1>
      </div>
      <div class="article-meta">
        <span>分类: {{ article.category?.name }}</span>
        <span>发布时间: {{ formatTime(article.createTime) }}</span>
      </div>
      <div class="article-content" v-html="article.content"></div>
    </el-card>

    <!-- 评论区域 -->
    <div class="comment-section">
      <h3>评论区</h3>
      <!-- 评论表单 -->
      <el-form :model="commentForm" label-width="80px" @submit.prevent="submitComment">
        <el-form-item label="昵称">
          <el-input v-model="commentForm.author" required></el-input>
        </el-form-item>
        <el-form-item label="评论内容">
          <el-input type="textarea" v-model="commentForm.content" rows="4" required></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit">提交评论</el-button>
        </el-form-item>
      </el-form>

      <!-- 评论列表 -->
      <div class="comment-list">
        <el-card v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-author">{{ comment.author }}</div>
          <div class="comment-time">{{ formatTime(comment.createTime) }}</div>
          <div class="comment-content">{{ comment.content }}</div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios'
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'ArticleView',
  setup() {
    const route = useRoute()
    const articleId = ref(route.params.id)
    const article = ref({})
    const comments = ref([])
    const commentForm = ref({
      author: '',
      content: ''
    })

    // 获取文章详情
    const fetchArticle = () => {
      axios.get(`/articles/${articleId.value}`).then(data => {
        article.value = data
        // 增加阅读量
        axios.post(`/articles/${articleId.value}/view`)
      })
    }

    // 获取评论列表
    const fetchComments = () => {
      axios.get(`/articles/${articleId.value}/comments`).then(data => {
        comments.value = data
      })
    }

    // 提交评论
    const submitComment = () => {
      axios.post('/comments', {
        ...commentForm.value,
        articleId: articleId.value
      }).then(() => {
        fetchComments()
        commentForm.value = { author: '', content: '' }
        ElMessage.success('评论提交成功，等待审核~')
      })
    }

    const formatTime = (time) => {
      return new Date(time).toLocaleString()
    }

    onMounted(() => {
      fetchArticle()
      fetchComments()
    })

    // 监听路由参数变化（用于同组件跳转）
    watch(() => route.params.id, (newId) => {
      articleId.value = newId
      fetchArticle()
      fetchComments()
    })

    return {
      article,
      comments,
      commentForm,
      formatTime,
      submitComment
    }
  }
}
</script>

<style scoped>
.article-detail {
  max-width: 1000px;
  margin: 20px auto;
  padding: 0 20px;
}

.article-meta {
  color: #666;
  margin: 10px 0 20px;
  display: flex;
  gap: 20px;
}

.article-content {
  line-height: 2;
  font-size: 16px;
}

.comment-section {
  margin-top: 40px;
}

.comment-list {
  margin-top: 20px;
}

.comment-item {
  margin-bottom: 10px;
}

.comment-author {
  font-weight: bold;
}

.comment-time {
  font-size: 12px;
  color: #999;
  margin: 5px 0;
}
</style>