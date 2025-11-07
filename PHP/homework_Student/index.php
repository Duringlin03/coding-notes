<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <form id="form1" name="form1" method="post" action="index_ok.php" onsubmit="return checkform(form1)">
        <fieldset style="width:500px">
            <legend style="font-size:16px">用户添加</legend>
            <table width="300" border="0" align="center">
                <tr>
                    <td width="77" align="right">姓名:</td>
                    <td width="213"><input name="name" type="text" id="name" size="24" /></td>
                </tr>
                <tr>
                    <td align="right">年龄:</td>
                    <td><input name="age" type="text" id="age" size="25" /></td>
                </tr>
                <tr>
                    <td>&nbsp;</td>
                    <td><input type="submit" name="sub" value="添加" />
                        <input type="reset" name="res" value="重置" />
                    </td>
                </tr>
            </table>
        </fieldset>
    </form>
    <div>
        <a href="show.php">
            <input type="button" value="管理所有用户" />
        </a>
    </div>
</body>

</html>