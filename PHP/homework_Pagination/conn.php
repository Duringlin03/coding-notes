<?php
$conn = mysqli_connect("localhost:3307","root","111","school")
    or die("连接数据库服务器失败!");

mysqli_query($conn, "set names utf8");
?>