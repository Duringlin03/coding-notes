<?php
header("Content-type:text/html;charset=utf-8");
include_once("conn.php");
if(count($_POST['chk'])==0){
    echo "<script>alert('请选择记录！');history.back(-1);</script>";
}else{
    for($i = 0;$i<count($_POST['chk']);$i++){
        $sqlstrl = "delete from student where id=".$_POST['chk'][$i];
        $result = mysqli_query($conn,$sqlstrl);
    }
    echo "<script>alert('删除成功！');location.href='show.php';</script>";
}
?>