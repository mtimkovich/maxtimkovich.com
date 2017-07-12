function randCaps (str) {
    return str.replace(/./g, (c) =>
        Math.random() > .5 ? c.toUpperCase() : c.toLowerCase()
    );
}

function getRandCaps () {
    var input = document.getElementById('text').value;
    document.getElementById('result').textContent = randCaps(input);

    return false;
}
