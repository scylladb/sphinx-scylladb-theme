function setCookie(name, value) {
	var date = new Date();
	date.setTime(date.getTime()+(60*24*60*60*1000));
	var expires = "; expires="+date.toGMTString();
	document.cookie = name+"="+value+expires+"; path=/";
	return value;
}

function getCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) {
			return c.substring(nameEQ.length,c.length);
		}
	}
	return '';
}

if (window.location.pathname == '/download-form-complete/') {
	setCookie('form-seen', 'form-seen');
	var dest = getCookie('scylla-destination');
	if (!dest) {
		dest = '/download/'
	}
	window.location.href = dest;
}

function showForm() {
	$('#download_signup').foundation('reveal', 'open');
	if(window.ga && ga.loaded) {
		ga('send', 'event', 'downloadForm', 'show');
	}
}

function resetForm() {
	setCookie('form-seen', 'form-reset');
}

if (window.location.pathname == '/download-form-complete/') {
	setCookie('form-seen', 'form-seen');
	var dest = getCookie('scylla-destination');
	if (!dest) {
		dest = '/download/'
	}
	window.location.href = dest;
}

if (window.location.pathname == '/welcome-newsletter/') {
	setCookie('form-seen', 'form-seen');
	window.location.href = '/doc/getting-started/';
}

function isFormPage() {
	if (document.getElementById('download_signup')) {
		return true;
	}
}

function maybeShowForm() {
	if (window.innerWidth < 1024) {
		return;
	}

	if (getCookie('cookie-test') != 'cookie-test') {
		setCookie('cookie-test', 'cookie-test');
		return;
	}

	if (!isFormPage()) {
		return;
	}

	if (getCookie('form-seen') == 'form-seen') {
		// refresh cookie for repeat visitors
		setCookie('form-seen', 'form-seen');
		return;
	}

	setCookie('scylla-destination', window.location.pathname);
    	showForm();
}

// To temporarily disable the download form, comment
// out the line below.
window.addEventListener('load', maybeShowForm);
