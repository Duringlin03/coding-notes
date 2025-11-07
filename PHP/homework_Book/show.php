<?php
session_start();
header("Content-type:text/html;charset=utf-8");
include("conn.php");

$sql = "SELECT * FROM tb_demo01";
$result = mysqli_query($conn, $sql);

if (!$result) {
    die("查询失败: " . mysqli_error($conn));
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>所有图书</title>
</head>
<body>
    <h2>已添加的图书列表</h2>
    <table border="1" cellpadding="10" cellspacing="0">
        <tr>
            <th>ID</th>
            <th>图书名称</th>
            <th>价格</th>
            <th>出版日期</th>
            <th>类型</th>
            <th>操作</th>
        </tr>
        <?php
        while ($row = mysqli_fetch_assoc($result)) {
        ?>
        <tr>
            <td><?php echo $row['id']; ?></td>
            <td><?php echo $row['name']; ?></td>
            <td><?php echo $row['price']; ?></td>
            <td><?php echo $row['date']; ?></td>
            <td><?php echo $row['type']; ?></td>
            
        </tr>
        <?php
        }
        mysqli_free_result($result);
        mysqli_close($conn);
        ?>
    </table>
    <br>
    <a href="index.php">返回添加页面</a>
</body>
</html>