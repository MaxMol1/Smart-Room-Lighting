/* Vue object */
var songdata = new Vue({
    el: "#songdata",
    data: {
        name : '',
        artist : '',
        lyrics : '',
        date : '',
        genre : '',
        pop : ''
    },
    methods: {
        change_song: function (name, artist, lyrics, date, genre, pop) {
            this.name = name
            this.artist = artist
            this.lyrics = lyrics
            this.date = date
            this.genre = genre
            this.pop = pop
        }
    }
});

const delay = ms => new Promise(res => setTimeout(res, ms));
var abort;

function set_abort() {
    abort = true;
}

async function start_tracking() {
    abort = false

    while (true) {
        if (abort)
            break

        console.log("fetching song...")

        let temp_data
        await $.ajax("/track").done(async function (data) {
            temp_data = data;
        });

        songdata.change_song(temp_data.name, temp_data.artist, temp_data.lyrics, temp_data.date, "none", temp_data.pop);    
        // Wait two seconds
        await delay(2000);
    }
}
