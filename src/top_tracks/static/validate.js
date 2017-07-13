function validate() {
    var artist = document.getElementById('artist').value;
    var error = document.getElementById('error');

    if (artist.indexOf('soundcloud.com/') != -1) {
        var pattern = new RegExp('soundcloud\.com/([^/]*)');
        var match = pattern.exec(artist);

        if (match == null) {
            error.innerText = 'Invalid username: "' + artist + '"';
            return false;
        }

        artist = match[1];
    }

    var r = Boolean(artist.match(/^[a-z0-9_-]+$/i));

    if (!r) {
        error.innerText = 'Invalid username: "' + artist + '"';
    }

    return r;
}
