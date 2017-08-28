var characters = {
    ' ': '-----',
    '.': '00001',
    '!': '11101',
    a: '75755',
    b: '75757',
    c: '71117',
    d: '35553',
    e: '71717',
    f: '71711',
    g: '71757',
    h: '55755',
    i: '72227',
    j: '44457',
    k: '55355',
    l: '11117',
    m: '57555',
    n: '75555',
    o: '75557',
    p: '75711',
    q: '75744',
    r: '75355',
    s: '71747',
    t: '72222',
    u: '55557',
    v: '55552',
    w: '55575',
    x: '55255',
    y: '55222',
    z: '74717',
};

var display = {
    7: 'ccc',
    5: 'c c',
    4: '  c',
    3: 'cc ',
    2: ' c ',
    1: 'c  ',
    0: '   ',
};


function printer(word, emote) {
    var output = '';
    for (var i = 0; i < 5; i++) {
        for (var c of word) {
            var line = characters[c][i];

            if (line == '-') {
                output += '  ';
                continue;
            }

            var print = display[line];

            print = print.replace(/ /g, ':blank:');
            print = print.replace(/c/g, emote);

            output += print + '  ';
        }

        output += '\n';
    }

    return output;
}

function slack() {
    var text = $('#text').val().toLowerCase();
    var emote = $('#emote').val();

    $('#result').val(printer(text, emote));
}
