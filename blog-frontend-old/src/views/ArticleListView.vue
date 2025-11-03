<template>
    <div class="article-list-container">
        <!-- 添加调试信息 -->
        <div v-if="debugMode">
            <p>加载状态: {{ loading }}</p>
            <p>错误信息: {{ error }}</p>
            <p>文章数量: {{ articles.length }}</p>
            <p>文章数据: {{ JSON.stringify(articles) }}</p>
        </div>
    </div>
    <div class="article-list-container">
        <!-- 页面标题 -->
        <div class="page-header">
            <h1>所有文章</h1>
            <p>共 {{ articles.length }} 篇文章</p>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>正在加载文章...</p>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="error" class="error-state">
            <p>❌ 加载失败: {{ error }}</p>
            <button @click="loadArticles" class="retry-btn">重试</button>
        </div>

        <!-- 文章列表 -->
        <div v-else class="articles-grid">
            <article v-for="article in articles" :key="article.id" class="article-card"
                @click="navigateToArticle(article.id)">
                <div class="article-header">
                    <h2 class="article-title">{{ article.title }}</h2>
                    <span class="article-category">{{ article.category?.name || '未分类' }}</span>
                </div>

                <div class="article-meta">
                    <span class="views">👁️ {{ article.viewCount }} 阅读</span>
                    <span class="date">📅 {{ formatDate(article.createTime) }}</span>
                </div>

                <p class="article-excerpt">{{ truncateContent(article.content) }}</p>

                <div class="article-footer">
                    <button class="read-more-btn">阅读全文 →</button>
                </div>
            </article>
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && articles.length === 0" class="empty-state">
            <p>暂无文章，快去发布一篇吧！</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'


// 调试模式开关
const debugMode = ref(true);

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

const response = await axios.get('http://localhost:8080/api/articles')
// 路由实例
const router = useRouter()



// 响应式数据
const articles = ref<Article[]>([])
const loading = ref(true)
const error = ref('')

// 加载文章数据
const loadArticles = async () => {
    try {
        loading.value = true;
        const response = await axios.get('/http://localhost:8080/api/articles');

        // 添加数据验证
        console.log('API响应数据:', response.data);

        if (Array.isArray(response.data)) {
            articles.value = response.data;
        } else {
            throw new Error('返回数据格式不正确，期望数组类型');
        }
    } catch (err: any) {
        console.error('详细错误信息:', err.response || err);
        error.value = err.response?.data?.message || err.message;
    } finally {
        loading.value = false;
    }
}

// 跳转到文章详情
const navigateToArticle = (id: number) => {
    router.push(`/article/${id}`)
}

// 格式化日期
const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    })
}

// 截断内容摘要
const truncateContent = (content: string) => {
    const maxLength = 120
    return content.length > maxLength
        ? content.substring(0, maxLength) + '...'
        : content || '暂无内容'
}

// 组件挂载时加载数据
onMounted(() => {
    loadArticles()
})
</script>

<style scoped>
.article-list-container {
    border: 2px solid red;
    /* 临时添加以便定位 */
}

.article-list-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    margin-left: 270px;
    /* 为左侧导航栏留出空间 */
}

.page-header {
    text-align: center;
    margin-bottom: 3rem;
}

.page-header h1 {
    color: #2c3e50;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.page-header p {
    color: #7f8c8d;
    font-size: 1.1rem;
}

/* 加载状态 */
.loading-state {
    text-align: center;
    padding: 3rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

/* 错误状态 */
.error-state {
    text-align: center;
    padding: 3rem;
    color: #e74c3c;
}

.retry-btn {
    margin-top: 1rem;
    padding: 0.5rem 1.5rem;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.retry-btn:hover {
    background: #2980b9;
}

/* 文章网格 */
.articles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.article-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid #e0e0e0;
}

.article-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    border-color: #3498db;
}

.article-header {
    display: flex;
    justify-content: between;
    align-items: start;
    gap: 1rem;
    margin-bottom: 1rem;
}

.article-title {
    color: #2c3e50;
    font-size: 1.3rem;
    font-weight: 600;
    margin: 0;
    flex: 1;
}

.article-category {
    background: #e8f4fd;
    color: #3498db;
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    font-size: 0.85rem;
    font-weight: 500;
}

.article-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: #7f8c8d;
}

.article-meta span {
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

.article-excerpt {
    color: #555;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.article-footer {
    text-align: right;
}

.read-more-btn {
    background: none;
    border: none;
    color: #3498db;
    cursor: pointer;
    font-weight: 500;
    padding: 0.5rem;
}

.read-more-btn:hover {
    color: #2980b9;
    text-decoration: underline;
}

/* 空状态 */
.empty-state {
    text-align: center;
    padding: 3rem;
    color: #7f8c8d;
    font-size: 1.1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .article-list-container {
        margin-left: 0;
        padding: 1rem;
    }

    .articles-grid {
        grid-template-columns: 1fr;
    }

    .page-header h1 {
        font-size: 2rem;
    }
}
</style>