<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>SmartContractStudy</title>
<script>
function weakTypeVerify(){
	var a = 5;
	var b = "5";
	var c = b + a
	document.getElementById("demo").innerHTML=c;
}
</script>
</head>
<body>

<h1>JavaScript弱类型演示</h1>
<p id="demo">弱类型演示</p>

<button type="button" onclick="weakTypeVerify()">弱类型演示</button>

</body>
</html>