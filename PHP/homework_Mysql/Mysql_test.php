<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>显示数据库信息</title>
    <style>
        table { border-collapse: collapse; margin: 20px 0; }
        table, th, td { border: 1px solid #333; }
        th, td { padding: 10px 15px; }
        th { background-color: #f0f0f0; }
    </style>
</head>
<body>
    <h1>用户信息列表</h1>

    <?php
    // 显示错误信息
    error_reporting(E_ALL);
    ini_set('display_errors', 1);

    // 数据库连接信息
    $servername = "localhost:3307";
    $username = "root";
    $password = "111"; // 你的数据库密码
    $dbname = "my_db"; // 数据库名称

    // 创建连接
    $conn = new mysqli($servername, $username, $password, $dbname);

    // 检查连接
    if ($conn->connect_error) {
        die("连接失败: " . $conn->connect_error);
    }

    // 设置字符集
    $conn->set_charset("utf8");

    // 查询数据
    $sql = "SELECT id, name, email FROM users";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        // 输出数据表格
        echo "<table>";
        echo "<tr><th>ID</th><th>姓名</th><th>邮箱</th></tr>";
        
        // 循环输出每条记录
        while($row = $result->fetch_assoc()) {
            echo "<tr>";
            echo "<td>" . $row["id"] . "</td>";
            echo "<td>" . $row["name"] . "</td>";
            echo "<td>" . $row["email"] . "</td>";
            echo "</tr>";
        }
        echo "</table>";
    } else {
        echo "0 结果";
    }

    // 关闭连接
    $conn->close();
    ?>
</body>
</html>
