package com.darling.blog.service.impl;

import com.darling.blog.entity.Article;
import com.darling.blog.repository.ArticleRepository;
import com.darling.blog.service.ArticleService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional
public class ArticleServiceImpl implements ArticleService {

    private final ArticleRepository articleRepository;

    // 使用构造器注入（推荐方式）
    public ArticleServiceImpl(ArticleRepository articleRepository) {
        this.articleRepository = articleRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public List<Article> getAllArticles() {
        return articleRepository.findAll();
    }

    @Override
    @Transactional(readOnly = true)
    public Article getArticleById(Long id) {
        return articleRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("文章不存在，ID: " + id));
    }

    @Override
    public Article createArticle(Article article) {
        // 可以在这里添加业务逻辑验证
        return articleRepository.save(article);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Article> getArticlesByCategory(Long categoryId) {
        return articleRepository.findByCategoryId(categoryId);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Article> getPopularArticles(int limit) {
        return articleRepository.findPopularArticles(limit);
    }

    @Override
    public Article updateArticle(Long id, Article updatedArticle) {
        return articleRepository.findById(id)
                .map(article -> {
                    // 只更新允许修改的字段
                    article.setTitle(updatedArticle.getTitle());
                    article.setContent(updatedArticle.getContent());
                    // 注意：分类更新需要额外处理
                    if (updatedArticle.getCategory() != null) {
                        article.setCategory(updatedArticle.getCategory());
                    }
                    return articleRepository.save(article);
                })
                .orElseThrow(() -> new RuntimeException("文章不存在，ID: " + id));
    }

    @Override
    public void deleteArticle(Long id) {
        if (!articleRepository.existsById(id)) {
            throw new RuntimeException("文章不存在，ID: " + id);
        }
        articleRepository.deleteById(id);
    }

    @Override
    public void incrementViewCount(Long id) {
        articleRepository.findById(id).ifPresent(article -> {
            article.setViewCount(article.getViewCount() + 1);
            articleRepository.save(article);
        });
    }
}