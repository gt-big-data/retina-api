function loadFeeds() {
	$.ajax({url: "/article/feeds", success: function(data) {
			buildFeeds(data);
		}
	});
}
function toggleFeed(feed, which) {
	$.ajax({url: '/feed/updateStatus/'+which+'?url='+encodeURIComponent(feed), success: function(data) {
			buildFeeds(data);
	}});	
}
$('#form1').submit(function(event) {
	event.preventDefault();

});
function buildFeeds(data) {
	$('.feedRow').remove();
	feeds = JSON.parse(data); html = '';
	for(i in feeds) {
		feed = feeds[i];
		html += '<div class="feedRow">'+feed['feed']+' <img src="/static/images/'+(feed['active']?'play':'pause')+'.png" alt="1" class="pausePlay" onclick="toggleFeed(\''+feed['feed']+'\', '+!feed['active']+');" /></div>';
	}
	$('#mainTable').append(html);
}
$(document).ready(function() {
	loadFeeds();
});