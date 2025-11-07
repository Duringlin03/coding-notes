<?php
$year = date("Y");
$month = date("m");
$day = date("j");
$wd_ar = array("周日", "周一", "周二", "周三", "周四", "周五", "周六");
$wd = date("w", mktime(0, 0, 0, $month, 1, $year));

echo "<table cellpadding=6 cellspacing=0 width=400 bgcolor=#bbffff>
        <tr align=center bgcolor=white> <td colspan=7>$year 年 $month 月";
// 输出星期
echo "<tr align=center >";
for ($i = 0; $i < 7; $i++) {
    echo "<td>" . $wd_ar[$i] . "</td>";
}
echo "</tr>";

// 输出日期
// 在这里date("t", mktime(0, 0, 0, $month, 1, $year)) 获取当前月份的天数
// $wd为星期数
// $tnum为当前月份的天数加上前面空白的天数
/*例如：
1月1日是星期五，那么$wd=5
1月31日是星期六，那么$tnum=31+5=36
1月1日是星期六，那么$tnum=1+5=6
1月7日是星期六，那么$tnum=7+5=12
1月14日是星期六，那么$tnum=14+5=19
1月21日是星期六，那么$tnum=21+5=26

*/
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