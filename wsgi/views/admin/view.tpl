<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Administrative view</title>
	% include('components/analytics.tpl')
</head>
<body>
	<h1>Administrator page</h1>
	<p>Mostly for my internal usage, not really much to wreck anyway</p>

	<h3>Audit log</h3>
	<table>
		<thead>
			<tr>
				<th>Timestamp</th>
				<th>Action</th>
				<th>Details</th>
				<th>IP</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>n/a</td>
				<td>n/a</td>
				<td>n/a</td>
				<td>n/a</td>
			</tr>
		</tbody>
	</table>

	<h3>Actions</h3>
	<form action="/admin/fetch/posts" method="post">
		<div>
			<input type="checkbox" name="purge_database" id="purge_database"><label for="purge_database">Drop existing DB</label>
		</div>
		<div>
			<button>Refresh blog posts</button>
		</div>
	</form>
</body>
</html>