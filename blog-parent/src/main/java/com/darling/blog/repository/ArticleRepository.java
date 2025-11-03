package com.darling.blog.repository;

import com.darling.blog.entity.Article;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

public interface ArticleRepository extends JpaRepository<Article, Long> {

    // 1. 根据分类ID查询文章（方法名自动解析）
    List<Article> findByCategoryId(Long categoryId);

    // 2. 根据标题关键词模糊查询（方法名自动解析）
    List<Article> findByTitleContaining(String keyword);

    // 3. 自定义查询：获取热门文章（按阅读量降序）
    @Query("SELECT a FROM Article a ORDER BY a.viewCount DESC LIMIT :limit")
    List<Article> findPopularArticles(@Param("limit") int limit);
}