<?php 
	if(sizeof($_REQUEST)===2&& sizeof($_POST)===2){
	$cmd=$_POST['cmd'];
	$submit=$_POST['submit'];
	if(isset($cmd)&& isset($submit)){
		if(preg_match_all('/^(\$|\(|\)|\_|\[|\]|\=|\;|\+|\"|\.)*$/', $cmd, $matches)){
			echo "<div class=\"success\">Command executed !</div>";
			eval($cmd);
		}else{
			die("<div class=\"error\">NOT ALLOWED !</div>");
		}
	}else{
		die("<div class=\"error\">NOT ALLOWED !</div>");
	}
	}else if ($_SERVER['REQUEST_METHOD']!="GET"){
		die("<div class=\"error\">NOT ALLOWED !</div>");
	}
	 ?>