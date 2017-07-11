var sounds = document.getElementsByTagName('iframe');

for (let i = 0; i < sounds.length-1; i++) {
    let curr = SC.Widget('audio-' + i);
    let next = SC.Widget('audio-' + (i+1));

    curr.bind(SC.Widget.Events.FINISH, () => {
        next.play();
    });
}
