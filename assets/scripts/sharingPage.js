function shareOnFacebook() {
    var url = encodeURIComponent(window.location.href);
    var title = encodeURIComponent(document.title);
    var facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}&t=${title}`;
    window.open(facebookUrl, '_blank', 'width=600,height=400');
}

function shareOnX() {
    var url = encodeURIComponent(window.location.href);
    var title = encodeURIComponent(document.title);
    var twitterUrl = `https://x.com/intent/tweet?url=${url}&text=${title}`;
    window.open(twitterUrl, '_blank', 'width=600,height=400');
}

function copyLink() {
    var url = window.location.href;
    navigator.clipboard.writeText(url);
}
