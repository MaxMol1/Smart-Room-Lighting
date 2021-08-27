/* Vue object */
var songData = new Vue({
    el: "#songData",
    data: {
        name : '',
        date : '',
        cover: '',
        pop : '',
        lyrics : '',
        genre : '',
        primaryColor : {
            'r' : 236,
            'g' : 240,
            'b' : 241
        },
        secondaryColor : {
            'r' : 236,
            'g' : 240,
            'b' : 241
        }
    },
    computed: {
        createGradient() {
            return `linear-gradient(45deg, rgba(${this.primaryColor.r}, ${this.primaryColor.g}, ${this.primaryColor.b}, 1) 0%, rgba(${this.secondaryColor.r}, ${this.secondaryColor.g}, ${this.secondaryColor.b}, 1) 100%)`;
        }
    },
    methods: {
        changeSong: function (name, artist, date, cover, pop, genre, lyrics, primaryColor, secondaryColor) {
            this.name = name + ' - ' + artist;
            this.date = date;
            this.cover = cover;
            this.pop = pop;
            this.genre = genre;
            this.lyrics = (lyrics === '') ? 'Lyrics not found ...' : lyrics;
            this.primaryColor = primaryColor;
            this.secondaryColor = secondaryColor;
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
                songData.changeSong(data.name, data.artist, data.date, data.cover, data.pop, data.genres[0], data.lyrics, data.primaryColor, data.secondaryColor);
                console.log('received both' + data.primaryColor + data.secondaryColor)
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
