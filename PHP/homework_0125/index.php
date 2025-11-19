<?php
session_start();
if (!isset($_SESSION['login_ok'])) {
    header("Location: login.php");
    exit;
}
require 'conn.php';
?>

<html>

<head>
    <meta charset="utf8">
    <title>图书信息</title>
</head>

<body>


    <form method="post" action="delete.php">
        <table width="800" border="1" align="center" cellpadding="8" cellspacing="0">
            <tr>
                <td colspan="6" align="center" bgcolor="#CCCCCC" style="color:blue">图书信息表</td>
            </tr>
            <tr>
                <th>编号</th>
                <th>图书书名</th>
                <th>作者</th>
                <th>出版社</th>
                <th>价格</th>
                <th>删除</th>
            </tr>

            <?php
            $sql = "SELECT * FROM book0125 ORDER BY id";
            $rs = mysqli_query($conn, $sql);
            while ($row = mysqli_fetch_array($rs)) {
                echo "<tr align='center'>";
                echo "<td>" . $row['id'] . "</td>";
                echo "<td>" . $row['title'] . "</td>";
                echo "<td>" . $row['author'] . "</td>";
                echo "<td>" . $row['publisher'] . "</td>";
                echo "<td>" . $row['price'] . "</td>";
                echo "<td><input type='checkbox' name='ids[]' value='" . $row['id'] . "'></td>";
                echo "</tr>";
            }
            ?>
            <tr>
                <td colspan="6" align="right">
                    <input type="submit" value=" 删 除 " onclick="return confirm('确定要删除选中的图书吗？');">
                </td>
            </tr>
        </table>
    </form>
</body>

</html>