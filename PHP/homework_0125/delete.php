<?php
session_start();
if (!isset($_SESSION['login_ok'])) {
    header("Location: login.php");
    exit;
}
require 'conn.php';

if (isset($_POST['ids']) && !empty($_POST['ids'])) {
    foreach ($_POST['ids'] as $id) {
        $id = intval($id);
        mysqli_query($conn, "DELETE FROM book0125 WHERE id=$id");
    }
    echo "<script>
    alert('批量删除成功!');
    location.href='index.php';
    </script>";
} else {
    echo "<script>
    alert('请至少选择一条记录!');
    location.href='index.php';
    </script>";
}
?>