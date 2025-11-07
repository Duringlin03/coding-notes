<?php
session_start();
if (!isset($_SESSION['time'])) {
    echo "<script>alert('您无权限查看本页面,请先登录!');location='index.php';</script>";
} elseif ((time() - $_SESSION['time']) < 600) {
    $_SESSION['time'] = time();
    ?>
    <table width="469" border="0" align="center">
        <tr>
            <td colspan="3"><img src="images/mysql_01.gif" width="464" height="139" /></td>
        </tr>
        <tr>
            <td width="81"><img src="images/mysql_02.gif" width="78" height="136" /></td>
            <td width="301" align="center" style="font-size: 24px; color:#CC00CC; font-weight: bolder">
                欢迎来到学涯在线!</td>
            <td width="74"><img src="images/mysql_04.gif" width="74" height="136" /></td>
        </tr>
        <tr>
            <td height="63" colspan="3"><img src="images/mysql_05.gif" width="464" height="61" /></td>
        </tr>
    </table>
    <?php
} else {
    echo "<script>alert('登录超时,请重新登录!');location='index.php';</script>";
}
?>