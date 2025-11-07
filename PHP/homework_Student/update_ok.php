<?php
header("COntent-type:text/html;charset=utf-8");
include_once("conn.php");
if ($_POST['action'] == "update") {
    if (!($_POST['id'] and $_POST['name'] and $_POST['age'])) {
        echo "输入不允许为空。点击<a href='javascript:history.back()'>这里</a>返回";
    } else {
        $sqlstr = "update student set name = '" . $_POST['name'] . "',age = '" . $_POST['age'] . "' where id = " . $_POST['id'];
        $result = mysqli_query($conn, $sqlstr);
        if ($result) {
            echo "修改成功。点击<a href='show.php'>这里</a>查看";
        } else {
            echo "修改失败。<br>$sqlstr";
        }
    }
}
?>