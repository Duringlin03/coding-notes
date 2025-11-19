<?php session_start(); ?>
<html>
<head>
<meta charset="utf8">
<title>登录</title>
</head>
<body>
<table width="400" border="1" align="center" cellpadding="10" cellspacing="0">
  <tr>
    <td colspan="2" align="left">
      用户登录
    </td>
  </tr>
  <form method="post">
  <tr>
    <td align="center">用户名：</td>
    <td><input type="text" name="username" size="25"></td>
  </tr>
  <tr>
    <td align="center">密　码：</td>
    <td><input type="password" name="password" size="25"></td>
  </tr>
  <tr>
    <td colspan="2" align="center" style="padding:15px;">
      <input type="submit" name="login" value=" 登 录 " >
      <input type="button" value=" 注 册 ">
    </td>
  </tr>
  </form>
</table>

<?php
if(isset($_POST['login'])){
    require 'conn.php';
    $u = $_POST['username'];
    $p = $_POST['password'];
    
    $sql = "SELECT * FROM user0125 WHERE username='$u' AND password='$p'";
    $rs = mysqli_query($conn, $sql);
    
    if(mysqli_num_rows($rs) > 0){
        $_SESSION['login_ok'] = true;
        header("Location: index.php");
        exit;
    } else {
        echo "<script>alert('用户名或密码错误！');</script>";
    }
}
?>
</body>
</html>