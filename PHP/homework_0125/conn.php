<?php
$conn = mysqli_connect("localhost:3307", "root", "111", "shop0125");

if (!$conn) {
    die("连接失败：" . mysqli_connect_error());
}

mysqli_query($conn, "SET NAMES utf8");
?>