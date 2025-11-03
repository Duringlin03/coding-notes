package com.darling.blog.service;

import com.darling.blog.entity.Article;
import java.util.List;

public interface ArticleService {
    Article createArticle(Article article);
    Article getArticleById(Long id);
    List<Article> getAllArticles();
    List<Article> getArticlesByCategory(Long categoryId);
    List<Article> getPopularArticles(int limit);
    Article updateArticle(Long id, Article article);
    void deleteArticle(Long id);
    void incrementViewCount(Long id);
}