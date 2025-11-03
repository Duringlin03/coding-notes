<!-- src/views/AboutView.vue -->
<template>
  <div class="about-container">
    <div class="about-content">
      <div class="about-header">
        <h1>关于我</h1>
        <p class="about-subtitle">分享技术，记录生活</p>
      </div>

      <div class="about-body">
        <div class="about-section">
          <h2>👋 你好，我是博主</h2>
          <p>
            欢迎来到我的个人博客！我是一名热爱技术的开发者，喜欢分享编程经验、学习心得和生活感悟。
            在这里，我会记录我的技术成长历程，分享一些有趣的项目和想法。
          </p>
        </div>

        <div class="about-section">
          <h2>💻 技术栈</h2>
          <div class="tech-stack">
            <span class="tech-tag">Vue.js</span>
            <span class="tech-tag">React</span>
            <span class="tech-tag">Node.js</span>
            <span class="tech-tag">Spring Boot</span>
            <span class="tech-tag">MySQL</span>
            <span class="tech-tag">Redis</span>
            <span class="tech-tag">Docker</span>
            <span class="tech-tag">Linux</span>
          </div>
        </div>

        <div class="about-section">
          <h2>📚 兴趣爱好</h2>
          <ul class="interests-list">
            <li>编程开发</li>
            <li>阅读技术书籍</li>
            <li>开源项目贡献</li>
            <li>摄影旅行</li>
            <li>音乐欣赏</li>
          </ul>
        </div>

        <div class="about-section">
          <h2>📬 联系方式</h2>
          <div class="contact-info">
            <div class="contact-item">
              <span class="contact-label">邮箱：</span>
              <span class="contact-value">contact@example.com</span>
            </div>
            <div class="contact-item">
              <span class="contact-label">GitHub：</span>
              <a href="https://github.com/username" class="contact-link">@username</a>
            </div>
            <div class="contact-item">
              <span class="contact-label">微博：</span>
              <a href="https://weibo.com/username" class="contact-link">@username</a>
            </div>
          </div>
        </div>

        <div class="about-section">
          <h2>🎯 博客目标</h2>
          <p>
            这个博客的建立是为了记录我的学习历程，分享有价值的技术内容，
            同时也希望能够帮助到其他在学习路上的朋友们。如果你有任何问题或建议，
            欢迎随时联系我！
          </p>
        </div>
      </div>

      <div class="about-footer">
        <div class="blog-stats">
          <div class="stat-item">
            <span class="stat-number">{{ totalArticles }}</span>
            <span class="stat-label">篇文章</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ totalCategories }}</span>
            <span class="stat-label">个分类</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ totalViews }}</span>
            <span class="stat-label">次阅读</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '@/utils/request'

const totalArticles = ref(0)
const totalCategories = ref(0)
const totalViews = ref(0)

onMounted(async () => {
  try {
    const [articlesRes, categoriesRes] = await Promise.all([
      request.get('/articles'),
      request.get('/categories')
    ])
    
    const articles = articlesRes.data || []
    const categories = categoriesRes.data || []
    
    totalArticles.value = articles.length
    totalCategories.value = categories.length
    totalViews.value = articles.reduce((sum, article) => sum + (article.viewCount || 0), 0)
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
})
</script>

<style scoped>
.about-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.about-content {
  background: white;
  border-radius: 12px;
  padding: 3rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.about-header {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid #e2e8f0;
}

.about-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 1rem;
}

.about-subtitle {
  font-size: 1.125rem;
  color: #718096;
}

.about-body {
  margin-bottom: 3rem;
}

.about-section {
  margin-bottom: 2.5rem;
}

.about-section h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 1rem;
}

.about-section p {
  color: #4a5568;
  line-height: 1.8;
  margin-bottom: 1rem;
}

.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.tech-tag {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-size: 0.875rem;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.tech-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.interests-list {
  list-style: none;
  padding: 0;
}

.interests-list li {
  color: #4a5568;
  padding: 0.5rem 0;
  position: relative;
  padding-left: 1.5rem;
}

.interests-list li::before {
  content: "•";
  color: #667eea;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.contact-item {
  display: flex;
  align-items: center;
}

.contact-label {
  font-weight: 500;
  color: #2d3748;
  min-width: 80px;
}

.contact-value {
  color: #4a5568;
}

.contact-link {
  color: #667eea;
  text-decoration: none;
  transition: color 0.3s ease;
}

.contact-link:hover {
  color: #5a67d8;
  text-decoration: underline;
}

.about-footer {
  border-top: 2px solid #e2e8f0;
  padding-top: 2rem;
}

.blog-stats {
  display: flex;
  justify-content: center;
  gap: 3rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
}

.stat-label {
  color: #718096;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .about-container {
    padding: 1rem;
  }
  
  .about-content {
    padding: 2rem;
  }
  
  .about-header h1 {
    font-size: 2rem;
  }
  
  .tech-stack {
    justify-content: center;
  }
  
  .blog-stats {
    gap: 2rem;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
}
</style>