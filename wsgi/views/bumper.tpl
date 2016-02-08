<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Mihai-Balan.info</title>
	<style>
	body {
		background-image: url(/static/img/chinese.jpg);
		background-clip: cover;
		background-position: center;
		margin: 0;
	}
	#banner {
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;
		height: 288px;
		width: 570px;
		margin: auto;
	}
	footer {
		background-color: rgba(249, 249, 249, 0.78);
		color: rgb(60, 60, 60);
		padding: .2em;
		text-align: center;
		position: fixed;
		bottom: 0;
		width: 100%;
		font-family: sans-serif;
	}
	</style>
	% include('components/analytics.tpl')
</head>
<body>
	<div id="banner">
		<img src="/static/img/bumper.min.svg" alt="">
	</div>
	<footer>© Mihai Balan, 2015 &bull; Sublime Text, &hearts; &amp; Inkscape &bull; Photo by <a href="https://www.flickr.com/photos/akaitori/2313895725/">akaitori</a></footer>
</body>
</html>