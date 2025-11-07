会使用字符串函数实现数据处理
会使用日期时间函数实现数据处理

任务一：从身份证号码中获取出生日期

从身份证号码中获取出生日期,字符串处理应用
- 身份证号码长度问题
- 截取的出生日期显示形式
- 根据显示形式确定截取字符串长度

实现
- 使用strlen()函数,确定身份证长度
- 使用substr()函数,截取出生日期

任务二:考研倒计时

假设2025年12月21日考研,编码实现考研倒计时
- 两个不同时间戳的比较
- 取出当前的系统时间戳
- 得到目标日期的时间戳
- 两个时间戳的差值,换算成天数输出

实现
- 使用time()函数,获取当前时间戳
- 使用mktime()函数,获取目标时间戳
- 使用abs()函数,计算两个时间戳的差值
- 使用floor()函数,将差值换算成天数
- 使用printf()函数,输出结果

2025年9月29日实训任务
会使用php文件的引用(A文件可以引用到B文件中的内容)
会使用日期时间函数实现日历制作


2025年9月30日
前端显示的东西上传到数据库中(MySQL)
设置数据类型 长度 年龄 性别
bookid name price author

主键  



php连接mysql注意事项
修改myini.ini文件,还要修改xampp的配置文件,将mysql的端口改为3308
地址已经改成: localhost:3308
username: root
password: 空 即 ""

在homework_Mysql文件夹中的Mysql_connect.php文件中,配置了连接数据库的代码
连接到详细的数据库和表的话,用include_once("Mysql_connect.php");
mysqli_select_db($conn,"school");这些代码来选择数据库和表就行
以后在php文件中,要连接数据库,就include_once("Mysql_connect.php");
然后就可以使用$conn这个变量来操作数据库了

关于修改端口以免冲突
xampp的mysql端口改为3308
直接打开"D:\xampp\phpMyAdmin\config.inc.php"
然后将里面的$cfg['Servers'][$i]['host'] = 改为'localhost:3308';
注意上面密码是空的,所以不用改

http://localhost/phpmyadmin/index.php

2025年10月21日
在phpmyadmin首页点击账户 修改localhost的root账户密码
然后在config.inc.php中设置密码 $cfg['Servers'][$i]['password'] = '111';
再将$cfg['Servers'][$i]['AllowNoPassword'] = false;
然后重新启动xampp的mysql服务
