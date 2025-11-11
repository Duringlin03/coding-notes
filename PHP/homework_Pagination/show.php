<?php
include_once("conn.php");
?>

<table width="90%" border="1" cellpadding="1" cellspacing="1" bordercolor="#FFFFFF" bgcolor="#CCCCCC">
    <tr>
        <td width="5%" height="25" align="center">id</td>
        <td width="30%" align="center">书名</td>
        <td width="10%" align="center">价格</td>
        <td width="20%" align="center">出版时间</td>
        <td width="10%" align="center">类别</td>
        <td width="10%" align="center">操作</td>
    </tr>
    <?php
    $pagesize = 3;
    $sqlstr = "select * from books order by id ";
    $result_total = mysqli_query($conn, $sqlstr);
    $totalNum = mysqli_num_rows($result_total);
    $pagecount = ceil($totalNum/$pagesize);
    (!isset($_GET['page']))?($page = 1):$page = $_GET['page'];
    ($page<= $pagecount)?$page:$page = $pagecount;
    $f_pageNum = ($page - 1) * $pagesize;
    $sqlstrl = $sqlstr . " limit " . $f_pageNum . "," . $pagesize;
    $result = mysqli_query($conn, $sqlstrl);
    while($rows = mysqli_fetch_array($result)){
    ?>
    <tr>
        <td width="5%" height="25" align="center" bgcolor="#FFFFFF"><?php echo $rows[0];?></td>
        <td width="30%" align="center" bgcolor="#FFFFFF"><?php echo $rows[1];?></td>
        <td width="10%" align="center" bgcolor="#FFFFFF"><?php echo $rows[2];?></td>
        <td width="20%" align="center" bgcolor="#FFFFFF"><?php echo $rows[3];?></td>
        <td width="10%" align="center" bgcolor="#FFFFFF"><?php echo $rows[4];?></td>
        <td width="10%" align="center" bgcolor="#FFFFFF">操作</td>
    </tr>
    <?php
    }
    ?>
<tr>
    <td height="25" colspan="6" align="left" bgcolor="#FFFFFF">&nbsp;&nbsp;
        <?php
        echo "共".$totalNum."条记录&nbsp;&nbsp;";
        echo "第".$page."页/共".$pagecount."页&nbsp;&nbsp;";
        if($page!=1){
            echo "<a href='show.php?page=1'>首页</a>&nbsp;";
            echo "<a href='show.php?page=".($page-1)."'>上一页</a>&nbsp;";
        }else{
            echo "首页&nbsp;上一页&nbsp;&nbsp;";
        }
        if($page!=$pagecount){
            echo "<a href='show.php?page=".($page+1)."'>下一页</a>&nbsp;";
            echo "<a href='show.php?page=".$pagecount."'>尾页</a>&nbsp;";
        }else{
            echo "下一页&nbsp;尾页&nbsp;";

        }
        ?>
    </td>
</tr>
</table>