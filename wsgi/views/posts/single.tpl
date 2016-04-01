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
			% if previous:
			<li class="previous">
				<a href="/posts/{{previous.base_path}}">{{previous.title}}</a>
			</li>
			% end
			% if next:
			<li class="next">
				<a href="/posts/{{next.base_path}}">{{next.title}}</a>
			</li>
			% end
		</ul>
	</nav>
	% include('components/footer.tpl')
</body>
</html>