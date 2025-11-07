<?php
header("Content-type:text/html;charset=utf-8");
include_once("conn.php");
if($_GET['action'] == "del"){
    $sqlstrl = "delete from student where id=".$_GET['id'];
    $result = mysqli_query($conn,$sqlstrl);
    if($result){
        echo "<script>alert('删除成功');location.href='show.php';</script>";
    }else{
        echo "删除失败";
    }
}
?>