<?hh
<<__EntryPoint>>
function main(): void {
	echo '
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	</head>
	<body>
		<div class="container">
		<form action="hack.php" method="POST">
			<h1> HAHA! You are now a prisoner! </h1>
			 <textarea class="form-control" name="cmd" rows="20"></textarea>
			<button type="submit" class="btn btn-primary">Submit</button>
		</form>
		</div>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script> 
	</body>
</html>
		';
}
