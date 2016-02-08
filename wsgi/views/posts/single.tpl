<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>{{title}}</title>
	<link href='https://fonts.googleapis.com/css?family=Cutive&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
	<link href='https://fonts.googleapis.com/css?family=Abril+Fatface&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
	<link href='https://fonts.googleapis.com/css?family=Patrick+Hand&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
	<link href='https://fonts.googleapis.com/css?family=Playfair+Display:400,400italic,700,700italic|Noto+Serif&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
	<link href='https://fonts.googleapis.com/css?family=Noto+Serif:400,400italic,700,700italic&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
	<link rel="stylesheet" href="/static/css/post.css">
</head>
<body>
	<!-- <header>
		<h1>Mihai Balan</h1>
		<h2>Thoughts <em>&</em> images</h2>
	</header> -->

	<article>
		{{!body.read()}}
	</article>
	<nav>
		<ul>
			<li>
				% if previous:
				<a href="/posts/{{previous.path}}">&larr; {{previous.title}}</a>
				% end
			</li>
			<li>
				% if next:
				<a href="/posts/{{next.path}}">{{next.title}} &rarr;</a>
				% end
			</li>
		</ul>
	</nav>
	<footer>© Mihai Balan, 2016</footer>
</body>
</html>