<?php
include_once("conn.php");
$sqlstrl = "select * from tb_demo01 order by id";
$result = mysqli_query($conn, $sqlstrl);
while ($rows = mysqli_fetch_row($result)) {
    echo "<table border='1' cellpadding='10' cellspacing='0' width='500' align='center'>";

    echo "<tr>";
    for ($i = 0; $i < count($rows); $i++) {
        echo "<td height='25' align='center' class='m_td'>" . $rows[$i] . "</td>";
    }
    echo "<td class='m_td'><a href='#'>修改</a>/<a href=delete.php?action=del&id=" . $rows[0] . " 
    onclick='return del()'>删除</a></td></br>";
    echo "</tr>";

    echo "</table>";
}
?>