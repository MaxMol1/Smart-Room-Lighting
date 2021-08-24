/* Vue object */
var songData = new Vue({
    el: "#songData",
    data: {
        name : '',
        lyrics : '',
        date : '',
        genre : '',
        pop : '',
        cover: ''
    },
    methods: {
        changeSong: function (name, artist, lyrics, date, genre, pop, cover) {
            this.name = name + ' - ' + artist;
            this.lyrics = lyrics;
            this.date = date;
            this.genre = genre;
            this.pop = pop;
            this.cover = cover;
        }
    }
});

const delay = ms => new Promise(res => setTimeout(res, ms));
var abort;

function showElements() {
    var hidden = document.getElementsByClassName('hide');
    for (i = 0; i < hidden.length; i++) {
        hidden[i].style.display = 'inline-block';
    }
}

function hideElements() {
    var hidden = document.getElementsByClassName('hide');
    for (i = 0; i < hidden.length; i++) {
        hidden[i].style.display = 'none';
    }
}

async function startTracking() {
    abort = false

    // swap buttons
    var trackBtn = document.getElementsByClassName('track-btn');
    var abortBtn = document.getElementsByClassName('abort-btn');
    trackBtn[0].style.display = 'none';
    abortBtn[0].style.display = 'inline-block';

    // start tracking
    while (true) {
        if (abort) {
            break;
        }

        console.log("fetching song ...");

        await $.ajax("/track").done(async function (data) {
            if (data['name'] !== '' & !abort) {
                songData.changeSong(data.name, data.artist, data.lyrics, data.date, '', data.pop, data.cover);
                showElements();
            }
        });

        // Wait two seconds
        await delay(2000);
    }
}

async function stopTracking() {
    // hide elements and stop tracking
    abort = true;
    hideElements();

    // swap buttons
    var trackBtn = document.getElementsByClassName('track-btn');
    var abortBtn = document.getElementsByClassName('abort-btn');
    trackBtn[0].style.display = 'inline-block';
    abortBtn[0].style.display = 'none';
}
