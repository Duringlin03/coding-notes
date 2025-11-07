<?php
session_start();
header("Content-type:text/html;charset=utf-8");
include("conn.php");

$sql = "SELECT * FROM student";
$result = mysqli_query($conn, $sql);

if (!$result) {
    die("查询失败: " . mysqli_error($conn));
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>所有用户</title>
</head>
<form method="post" action="deletes.php" onsubmit="return confirm('确定要删除选中的记录吗？')">
    <table border="1" cellpadding="10" cellspacing="0">
        <tr>
            <th>选择</th>
            <th>序号</th>
            <th>ID</th>
            <th>姓名</th>
            <th>年龄</th>
            <th>操作</th>
        </tr>
        <?php
        $index = 1;
        while ($row = mysqli_fetch_assoc($result)) {
            ?>
            <tr>
                <td>
                    <input type="checkbox" name="chk[]" value="<?php echo $row['id']; ?>">
                </td>
                <td><?php echo $index; ?></td>
                <td><?php echo $row['id']; ?></td>
                <td><?php echo $row['name']; ?></td>
                <td><?php echo $row['age']; ?></td>
                <td>
                    <a href="update.php?action=update&id=<?php echo $row['id']; ?>">编辑</a>/
                    <a href="delete.php?action=del&id=<?php echo $row['id']; ?>">删除</a>
                </td>
            </tr>
            <?php
            $index++;
        }
        mysqli_free_result($result);
        mysqli_close($conn);
        ?>
    </table>

    <br>
    <input type="submit" value="批量删除选中记录">
</form>

<!-- 全选/取消全选的JavaScript -->
<script>
    var checkAll = document.getElementById('checkAll');
    var checkboxes = document.getElementsByName('chk[]');
    checkAll.onchange = function () {
        checkboxes.forEach(function (checkbox) {
            checkbox.checked = checkAll.checked;
        });
    }
    checkboxes.forEach(function (checkbox) {
        checkbox.onchange = function () {
            var allChecked = Array.from(checkboxes).every(cb => cb.checked);
            checkAll.checked = allChecked;
        }
    });
</script>

<br>
<a href="index.php">返回添加页面</a>

</html>