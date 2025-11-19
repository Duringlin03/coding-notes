-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主机： localhost:3307
-- 生成日期： 2025-11-18 10:48:29
-- 服务器版本： 10.4.32-MariaDB
-- PHP 版本： 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `shop0125`
--

-- --------------------------------------------------------

--
-- 表的结构 `book0125`
--

CREATE TABLE `book0125` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `author` varchar(100) DEFAULT NULL,
  `publisher` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 转存表中的数据 `book0125`
--

INSERT INTO `book0125` (`id`, `title`, `author`, `publisher`, `price`) VALUES
(8, 'JavaScript权威指南', '王五', '机械工业出版社', 128.00),
(9, 'Linux命令行与shell脚本', '赵六', '电子工业出版社', 79.00),
(10, 'Python网络爬虫权威指南', '周七', '人民邮电出版社', 89.00),
(11, 'PHP从入门到精通', '张三', '清华大学出版社', 68.00),
(12, 'MySQL数据库开发', '李四', '人民邮电出版社', 55.00),
(13, 'JavaScript权威指南', '王五', '机械工业出版社', 128.00),
(14, 'Linux命令行', '赵六', '电子工业出版社', 79.00),
(15, 'Python网络爬虫', '周七', '人民邮电出版社', 89.00);

-- --------------------------------------------------------

--
-- 表的结构 `user0125`
--

CREATE TABLE `user0125` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 转存表中的数据 `user0125`
--

INSERT INTO `user0125` (`id`, `username`, `password`) VALUES
(1, '123', '123');

--
-- 转储表的索引
--

--
-- 表的索引 `book0125`
--
ALTER TABLE `book0125`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `user0125`
--
ALTER TABLE `user0125`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `book0125`
--
ALTER TABLE `book0125`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- 使用表AUTO_INCREMENT `user0125`
--
ALTER TABLE `user0125`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
