package com.darling.blog.controller;

import com.darling.blog.entity.Article;
import com.darling.blog.service.ArticleService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:5173") // 临时解决方案
@RestController
@RequestMapping("/api/articles")
public class ArticleController {

    private final ArticleService articleService;

    // 构造器注入
    public ArticleController(ArticleService articleService) {
        this.articleService = articleService;
    }

    // 1. 获取所有文章
    @GetMapping
    public List<Article> getAllArticles() {
        return articleService.getAllArticles();
    }

    // 2. 根据ID获取单篇文章
    @GetMapping("/{id}")
    public Article getArticleById(@PathVariable Long id) {
        return articleService.getArticleById(id);
    }

    // 3. 创建新文章
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Article createArticle(@RequestBody Article article) {
        return articleService.createArticle(article);
    }

    // 4. 更新文章
    @PutMapping("/{id}")
    public Article updateArticle(@PathVariable Long id, @RequestBody Article article) {
        return articleService.updateArticle(id, article);
    }

    // 5. 删除文章
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteArticle(@PathVariable Long id) {
        articleService.deleteArticle(id);
    }

    // 6. 获取热门文章
    @GetMapping("/popular")
    public List<Article> getPopularArticles(
            @RequestParam(defaultValue = "5") int limit) {
        return articleService.getPopularArticles(limit);
    }

    // 7. 增加阅读量
    @PostMapping("/{id}/view")
    public void incrementViewCount(@PathVariable Long id) {
        articleService.incrementViewCount(id);
    }
}