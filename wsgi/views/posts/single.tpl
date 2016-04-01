<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>{{title}}</title>
	% include('components/common_style.tpl')
	% include('components/analytics.tpl')
</head>
<body>
	<!-- <header>
		<h1>Mihai Balan</h1>
		<h2>Thoughts <em>&</em> images</h2>
	</header> -->
	% include('components/header.tpl')
	<article>
		{{!body.read()}}
	</article>
	<nav>
		<ul>
			<li>
				% if previous:
				<a href="/posts/{{previous.base_path}}">&larr;&nbsp;{{previous.title}}</a>
				% end
			</li>
			<li>
				% if next:
				<a href="/posts/{{next.base_path}}">{{next.title}}&nbsp;&rarr;</a>
				% end
			</li>
		</ul>
	</nav>
	% include('components/footer.tpl')
</body>
</html>