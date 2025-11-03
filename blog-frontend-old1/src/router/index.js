import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue' // 导入全局布局组件
import HomeView from '../views/HomeView.vue'
import ArticleView from '../views/ArticleView.vue'
import ArticleManage from '../views/admin/ArticleManage.vue'
import ArticleEdit from '../views/admin/ArticleEdit.vue'
import CategoriesView from '../views/CategoriesView.vue'
import AboutView from '../views/AboutView.vue'

const routes = [
  {
    path: '/',
    component: MainLayout, // 应用全局布局
    children: [
      {
        path: '',
        name: 'home',
        component: HomeView
      },
      {
        path: '/article/:id',
        name: 'article',
        component: ArticleView
      },
      {
        path: '/categories',
        name: 'categories',
        component: CategoriesView
      },
      {
        path: '/about',
        name: 'about',
        component: AboutView
      }
    ]
  },
  // 管理员页面也使用相同布局，保持导航一致性
  {
    path: '/admin',
    component: MainLayout,
    children: [
      {
        path: 'articles',
        name: 'articleManage',
        component: ArticleManage
      },
      {
        path: 'article-edit',
        name: 'articleEdit',
        component: ArticleEdit
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
    