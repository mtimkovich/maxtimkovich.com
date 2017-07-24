var digits = {
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
            5: 'five',
            6: 'six',
            7: 'seven',
            8: 'eight',
            9: 'nine'
};

var power = {
            1: 'hundred',
            2: 'thousand',
            3: 'million',
            4: 'billion',
            5: 'trillion',
            6: 'quadrillion'
};

var prefix = {
            3: 'thir',
            5: 'fif',
            8: 'eigh'
};

String.prototype.append = function (rest) {
    if (this.length == 0) {
        return rest;
    } else {
        return this + ' ' + rest;
    }
}

String.prototype.capitalize = function () {
    return this.charAt(0).toUpperCase() + this.slice(1).toLowerCase();
}

function tens (n) {
    if (n == 1) {
        return 'ten';
    } else if (n == 2) {
        return 'twenty';
    } else if (n in prefix) {
        return prefix[n] + 'ty';
    } else {
        return digits[n] + 'ty';
    }
}


function teens (n) {
    n %= 10;

    if (n == 1) {
        return 'eleven';
    } else if (n == 2) {
        return 'twelve';
    } else if (n in prefix) {
        return prefix[n] + 'teen';
    } else {
        return digits[n] + 'teen';
    }
}

function threes (num) {
    while (num.length % 3 != 0) {
        num = '0' + num;
    }

    var parts = [];

    for (var i = 0; i < num.length; i+=3) {
        parts.push(num.substring(i, i+3));
    }

    return parts;
}


function to_words (parts) {
    var output_parts = [];

    for (let part of parts) {
        var word = '';
        var digit = parseInt(part[0], 10);

        if (digit != 0) {
            word = word.append(digits[digit]).append(power[1]);
        }

        var ten = parseInt(part[1], 10);
        var one = parseInt(part[2], 10);
        var dd = parseInt(part.substring(1, 3));

        if (dd == 0) {
            // Nothing
        } else if (dd % 10 == 0) {
            word = word.append(tens(ten));
        } else if (dd < 10) {
            word = word.append(digits[dd]);
        } else if (dd < 20) {
            word = word.append(teens(dd));
        } else {
            word = word.append(tens(ten) + '-' + digits[one]);
        }

        output_parts.push(word);
    }

    return output_parts;
}

function concatenate (parts) {
    var output = '';
    var largest = parts.length;

    for (var i = 0; i < largest; i++) {
        output = output.append(parts[i]);

        if (i < largest - 1 && parts[i] != '') {
            output = output.append(power[largest-i] + ',');
        }

    }

    if (parts[largest-1] == '' || parts[largest-1].indexOf('hundred') == -1) {
        let c = output.lastIndexOf(',');
        output = output.substring(0, c) + output.substring(c+1);
    }


    return output;
}

function longhand (num) {
    if (num.search('0+') != -1) {
        return 'Zero';
    }

    var parts = threes(num);
    var words = to_words(parts);
    var output = concatenate(words);

    return output;
}

function getLonghand () {
    var input = document.getElementById('number').value;
    input = input.trim();

    var error_msg = document.getElementById('error_msg');

    if (!input || input.split('').some(isNaN) || input.length >= 19) {
        error_msg.textContent = 'Invalid number: ' + input;
        return false;
    } else {
        error_msg.textContent = '';
    }

    cardinal = longhand(input).capitalize();

    var result = document.getElementById('result');
    result.textContent = cardinal;

    return false;
}
