<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
<?php
$conn=mysqli_connect("localhost:3307","root","111")  or 
die("数据库连接失败".mysqli_error($conn));//连接到数据库
mysqli_query($conn,"set names utf8");//设置字符集

?>
</body>
</html>