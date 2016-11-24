/**
 * Fast UUID generator, RFC4122 version 4 compliant.
 * @author Jeff Ward (jcward.com).
 * @license MIT license
 * @link http://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid-in-javascript/21963136#21963136
 **/
var UUID = (function() {
  var self = {};
  var lut = []; for (var i=0; i<256; i++) { lut[i] = (i<16?'0':'')+(i).toString(16); }
  self.generate = function() {
    var d0 = Math.random()*0xffffffff|0;
    var d1 = Math.random()*0xffffffff|0;
    var d2 = Math.random()*0xffffffff|0;
    var d3 = Math.random()*0xffffffff|0;
    return lut[d0&0xff]+lut[d0>>8&0xff]+lut[d0>>16&0xff]+lut[d0>>24&0xff]+'-'+
      lut[d1&0xff]+lut[d1>>8&0xff]+'-'+lut[d1>>16&0x0f|0x40]+lut[d1>>24&0xff]+'-'+
      lut[d2&0x3f|0x80]+lut[d2>>8&0xff]+'-'+lut[d2>>16&0xff]+lut[d2>>24&0xff]+
      lut[d3&0xff]+lut[d3>>8&0xff]+lut[d3>>16&0xff]+lut[d3>>24&0xff];
  }
  return self;
})();

function setCookie(name, value, days) {
	var date = new Date();
	date.setTime(date.getTime()+(days*24*60*60*1000));
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

function refreshUserID(days) {
	var mkID = getCookie('_mkto_trk');
	if (mkID) {
		userID = mkID;
	} else {
		userID = getCookie('userID');
	}

	if (userID) {
		setCookie('userID', userID, days);
	} else {
		setCookie('userID', UUID.generate(), days);
	}
	if (typeof(ga) == 'function') {
		ga('set', 'userId', userID);
	}
}

function sendEvent(ev) {
	if (typeof(ga) == 'function') {
		ga('send', 'event', ev);
	}
}

function showForm() {
	sendEvent('showForm');
	document.getElementsByTagName('body')[0].style.overflow = 'hidden';
	$('#download_signup').foundation('reveal', 'open');
}

function resetForm() {
	refreshUserID(1);
	setCookie('form-seen', 'form-reset', 60);
}

function launchAMI() {
	sendEvent('launchAMI');
}

if (window.location.pathname == '/ghmp/') {
	setCookie('form-seen', 'form-reset', 60);
	refreshUserID(60);
	window.location.href = '/doc/getting-started/';
}

if (window.location.pathname == '/dghmb/') {
	setCookie('form-seen', 'form-seen', 365);
	window.location.href = '/doc/getting-started/';
}

if (window.location.pathname == '/download-form-complete/') {
	sendEvent('formComplete')
	setCookie('form-seen', 'form-seen', 60);
}

if (window.location.pathname == '/welcome-newsletter/') {
	setCookie('form-seen', 'form-seen', 60);
	window.location.href = '/doc/getting-started/';
}

if (window.location.pathname == '/download-scylla/') {
	if(getCookie('reg-wall') == 'reg-wall') {
		sendEvent('formComplete');
		setCookie('form-seen', 'form-seen', 60);
	}
	window.location.href = '/download/';
}

function isFormPage() {
	if (document.getElementById('download_signup')) {
		return true;
	} else {
		return false;
	}
}

function maybeShowForm() {
	if (window.innerWidth < 1024) {
		return;
	}

	if (!getCookie('userID')) {
		return;
	}

	if (!isFormPage()) {
		return;
	}

	if (getCookie('form-seen') == 'form-seen') {
		// refresh cookie for repeat visitors
		setCookie('form-seen', 'form-seen', 60);
		return;
	}

	setCookie('reg-wall', 'reg-wall', 1);
    	showForm();
}


function setUserID() {
	if (typeof(ga) == 'undefined' || typeof(ga.create) == 'undefined') {
		return;
	}
	refreshUserID(365);	
}

function hasCode(el) {
	if (el.tagName === "CODE") {
		return true;
	}
	var children = el.childNodes;
	for(var i = 0; i < children.length; i++) {
		if (hasCode(children[i])) {
			return true;
		}
	}
	return false;
}

function logSelection(e) {
	if (logSelection.done) {
		return
	} else {
		logSelection.done = true;
	}

	if (!isFormPage()) {
		return;
	}
	if (hasCode(e.target)) {
		console.log("code selected");
		sendEvent("selectDownload");
	}
}

function doLoad() {
	setUserID();
	maybeShowForm();
}

window.addEventListener("mouseup", logSelection);

// To temporarily disable the download form, comment
// out the line below.
window.addEventListener('load', doLoad);
