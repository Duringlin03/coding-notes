// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import ArticleView from '../views/ArticleView.vue'
import CategoriesView from '../views/CategoriesView.vue'
import ArticlePublish from '../views/ArticlePublish.vue'
import ArticleEdit from '../views/ArticleEdit.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/about', component: AboutView },
  { path: '/categories', component: CategoriesView },
  { path: '/article/:id', component: ArticleView },
  { path: '/category/:id', component: CategoriesView }, // 分类文章列表页
  { path: '/publish', component: ArticlePublish }, // 文章发布页
  { path: '/edit/:id', component: ArticleEdit } // 文章编辑页
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router