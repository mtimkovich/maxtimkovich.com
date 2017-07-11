function validate() {
    var artist = document.getElementById('artist').value;
    var r = Boolean(artist.match(/^[a-z0-9_-]+$/i));

    if (!r) {
        var error = document.getElementById('error');
        if (artist.match(/^\s*$/) == null) {
            error.innerText = 'Invalid username: ' + artist;
        } else {
            error.innerText = 'Invalid username';
        }
    }

    return r;
}
