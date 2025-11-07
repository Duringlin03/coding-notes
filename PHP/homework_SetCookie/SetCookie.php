<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <?php
    date_default_timezone_set("Asia/Shanghai");
    if (!isset($_COOKIE["visit_time"])) {
        setcookie("visit_time", date("Y-m-d H:i:s"), time() + 60);
        echo "欢迎您第一次访问网站！";
        echo "<br>";
    } else {
        setcookie("visit_time", date("Y-m-d H:i:s"), time() + 60);
        echo "您上次访问网站的时间为:" . $_COOKIE["visit_time"];
        echo "<br>";
    }

    echo "您本次访问网站的时间为:" . date("Y-m-d H:i:s");
    ?>
</body>

</html>