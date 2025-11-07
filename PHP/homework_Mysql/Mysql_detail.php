<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <?php
    //将结果返回数组
    include_once("Mysql_connect.php");
    mysqli_select_db($conn,"school");
    $result = mysqli_query($conn,"select * from book");
    echo"<table border='1'>";
    echo"<tr align=center><td align=center colspan=3>
    <b>图书信息</b></td></tr>";
    echo "<tr align=center><td>图书ID</td><td>图书名</td><td>价格</td></tr>";
    while($votearray=mysqli_fetch_array($result)){
        echo"<tr><td>{$votearray['bookId']}</td><td>{$votearray['name']}</td><td>{$votearray['price']}</td></tr>";
    }
    echo"</table>";
    ?>
</body>
</html>