/* Spotify API endpoints */
const currently_playing_endpoint = 'https://api.spotify.com/v1/me/player/currently-playing'

/* Get access token from redirect uri query string and set options for subsequent calls */
const querystring = String(window.location).split('#')[1];
const params = new URLSearchParams(querystring);
const ACCESS_TOKEN = params.get('access_token');
const options = {
    headers: {
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    }
};

/* Global vars */
var abort = true;

/* Vue object */
var songdata = new Vue({
    el: '#songdata',
    data: {
        name : '',
        artist : '',
        lyrics : '',
        date : '',
        genre : '',
        pop : ''
    },
    methods: {
        change_song: function (name, artist, date, genre, pop) {
            this.name = name
            this.artist = artist
            this.date = date
            this.genre = genre
            this.pop = pop
        }
    }
})

/* Get current song */
async function track_current_song() {
    const current_play_data = await (await fetch(currently_playing_endpoint, options)).json();
    const name = current_play_data.item.name;
    const artist = current_play_data.item.artists;
    const date = current_play_data.item.album.release_date;
    // const genre = current_play_data.item.artists;
    const pop = current_play_data.item.popularity;
    
    songdata.change_song(name, artist[0].name, date, "none", pop);
}

/* Start/Stop tracking function */
async function track_songs() {
    abort = false;
    console.log("started tracking...")
    
    const delay = ms => new Promise(res => setTimeout(res, ms));
    (async() => {
        while (abort === false) {
            track_current_song(options);
            await delay(5000);
        }
        console.log("stopped tracking...");
    })();
}
