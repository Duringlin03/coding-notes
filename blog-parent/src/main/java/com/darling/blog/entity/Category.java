package com.darling.blog.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;
import java.time.LocalDateTime;

@Entity
@Table(name = "t_category") // 映射到数据库表名
@Getter
@Setter
public class Category {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // 主键自增策略
    private Long id;

    @Column(nullable = false, length = 50) // 非空，长度50
    private String name;

    @CreationTimestamp
    @Column(name = "create_time", updatable = false) // 数据库列名，不可更新
    private LocalDateTime createTime;

    @UpdateTimestamp
    @Column(name = "update_time") // 数据库列名
    private LocalDateTime updateTime;

    // 可选：方便调试的toString方法
    @Override
    public String toString() {
        return "Category{" +
                "id=" + id +
                ", name='" + name + '\'' +
                '}';
    }
}