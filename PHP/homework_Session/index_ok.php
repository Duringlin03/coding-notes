<?php
session_start();
header("Content-type:text/html;charset=utf-8");
include("conn.php");
$name = $_POST["user"];
$pwd = $_POST["pwd"];
$sql = mysqli_query($conn, "select * from tb_member where name='{$name}' and password='{$pwd}'");
if (mysqli_num_rows($sql) > 0) {
    $_SESSION['name'] = $name;
    $_SESSION['time'] = time();
    echo "<script>alert('登录成功!');location='show.php';</script>";
} else {
    echo "<script>alert('用户名或密码错误');location='index.php';</script>";
}
?>