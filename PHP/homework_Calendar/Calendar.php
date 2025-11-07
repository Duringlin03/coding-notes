<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日历</title>
</head>

<body>
    <!-- 实现步骤:
    1.获取当前年月并处理参数
    2.计算关键日期信息
    3.构建日历HTML结构
    4.填充日期数据
    php下的日历实现主要是依靠php强大的时间、日期函数,包括date(),mktime()函数等,
    
    - 获取当月的天数
    - 当月的第一天是星期几
    - 控制日期在表格中的对应输出
    
    -->
    <?php
    $year = date("Y");
    $month = date("m");
    $day = date("j");
    $wd_ar = array("周日", "周一", "周二", "周三", "周四", "周五", "周六");
    $wd = date("w", mktime(0, 0, 0, $month, 1, $year));
    echo "<table cellpadding=6 cellspacing=0 width=400 bgcolor=#bbffff>
        <tr align=center bgcolor=#cccccc>";
    echo "<tr align=center>";
    for ($i = 0; $i < 7; $i++) {
        echo "<td>" . $wd_ar[$i] . "</td>";
    }
    echo "</tr>";
    $tnum = $wd + date("t", mktime(0, 0, 0, $month, 1, $year));
    for ($i = 0; $i < $tnum; $i++) {
        $date = $i + 1 - $wd;
        if ($i % 7 == 0) {
            echo "<tr align=center>";
        }
        echo "<td>";
        if ($i >= $wd) {
            if ($date == $day && $month == date("m") && $year == date("Y")) {
                echo "<b><font color=red>" . $date . "</font></b>";
            } else {
                echo $date;
            }
            echo "</td>";
            if ($i % 7 == 6)
                echo "</tr>";
        }
    }
    echo "</table>";
    ?>
</body>

</html>