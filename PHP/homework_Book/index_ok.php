<?php
session_start();
header("Content-type:text/html;charset=utf-8");
include("conn.php");
$name = $_POST["name"];
$price = $_POST["price"];
$date = $_POST["date"];
$type = $_POST["type"];
if (!($_POST['name'] and $_POST['price'] and $_POST['date'] and $_POST['type'])) {
    echo "输入不允许为空.点击<a href='javascript:history.go(-1)'>这里</a>返回重试.";
} else {
    $sqlstrl = "insert into tb_demo01 values('','" . $_POST['name'] . "',
    '" . $_POST['price'] . "','" . $_POST['date'] . "','" . $_POST['type'] . "')";
    $result = mysqli_query($conn, $sqlstrl);
    if ($result) {
        echo "添加成功!点击<a href='index.php'>这里</a>继续添加.";
    } else {
        echo "添加失败!点击<a href='javascript:history.go(-1)'>这里</a>返回重试.";
    }
}
?>