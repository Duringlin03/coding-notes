package com.darling.blog.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;
import java.time.LocalDateTime;

@Entity
@Table(name = "t_article")
@Getter
@Setter
public class Article {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100) // 文章标题
    private String title;

    @Column(name = "view_count",columnDefinition = "INT DEFAULT 0")
    private Integer viewCount;

    @Lob // 标记为大型对象（对应MySQL的LONGTEXT）
    @Column(nullable = false, columnDefinition = "LONGTEXT")
    private String content;

    @ManyToOne // 多篇文章属于一个分类
    @JoinColumn(name = "category_id", nullable = false) // 外键列
    private Category category;

    @CreationTimestamp
    @Column(name = "create_time", updatable = false)
    private LocalDateTime createTime;

    @UpdateTimestamp
    @Column(name = "update_time")
    private LocalDateTime updateTime;

    // 可选：toString方法
    @Override
    public String toString() {
        return "Article{" +
                "id=" + id +
                ", title='" + title + '\'' +
                '}';
    }
}