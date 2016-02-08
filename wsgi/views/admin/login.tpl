<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Administrative page</title>
	<meta name="google-signin-scope" content="profile email">
	<meta name="google-signin-client_id" content="872165141587-0jiqclkhvf6f4dj6scm4bvaidgpbh4s7.apps.googleusercontent.com">
	<script src="https://apis.google.com/js/platform.js" async defer></script>
	% include('components/analytics.tpl')
</head>
<body>
	<div class="g-signin2" data-onsuccess="onSignIn" data-theme="dark"></div>
	<div id="response">Server says <span id="result"></span></div>
	<script>
	function onSignIn(googleUser) {
		var id_token = googleUser.getAuthResponse().id_token;
		document.querySelector('#idtoken').value = id_token;
		document.querySelector('#login').submit();
	};
	</script>
	<form action="/admin/check" id="login" method="post"><input type="hidden" name="idtoken" id="idtoken"></form>
</body>
</html>