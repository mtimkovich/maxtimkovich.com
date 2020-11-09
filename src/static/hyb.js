const synonyms = {
    hell: ['hell', 'heck', 'inferno', 'misery', 'nightmare', 'purgatory',
        'Hades', 'abyss', 'blazes', 'perdition', 'underworld',
        'bottomless pit', 'everlasting fire', 'fire and brimstone',
        'hell-fire', 'infernal regions', 'lower world', 'nether world',
        'place of torment'
    ],
    yeah: ['yeah', 'yes', 'affirmative', 'amen', 'true', 'yep',
        'okay', 'fine'
    ],
    brother: ['brother', 'twin', 'kin', 'kinsperson', 'relation', 'sibling',
        'sister', 'bro', 'sis'
    ],
};

function sample(array) {
    return array[Math.floor(Math.random() * array.length)];
}

function hellYeah() {
    const phrase = ['hell', 'yeah', 'brother'];
    const thesaurize = phrase.map(word => sample(synonyms[word])).join(' ');

    return thesaurize;
}

const yes = hellYeah();
document.title = yes;
document.write(yes);
