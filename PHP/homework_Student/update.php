<?php
include_once("conn.php");
if ($_GET['action'] == "update") {
    $sqlstr = "select * from student where id =" . $_GET['id'];
    $result = mysqli_query($conn, $sqlstr);
    $rows = mysqli_fetch_row($result);
}
?>

<form name="intFrom" method="post" action="update_ok.php">
    姓名：<input type="text" name="name" value="<?php echo $rows[1]; ?>"><br>
    年龄：<input type="text" name="age" value="<?php echo $rows[2]; ?>"><br>
    <input type="hidden" name="action" value="update">
    <input type="hidden" name="id" value="<?php echo $rows[0]; ?>">
    <input type="submit" name="submit" value="修改">
    <input type="reset" name="reset" value="重置">
</form>