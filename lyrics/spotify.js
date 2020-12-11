const fetch = require("node-fetch")

var currentlyPlayingEndpoint = 'https://api.spotify.com/v1/me/player/currently-playing'
var trackEndpoint = 'https://api.spotify.com/v1/tracks/'
var analysisEndpoint = 'https://api.spotify.com/v1/audio-analysis/'
var accessToken = ''
var options = {
    headers: {
      'Authorization': accessToken
    }
};

async function main() {
    const currentPlayData = await (await fetch(currentlyPlayingEndpoint, options)).json();
    const trackId = currentPlayData.item.id

    const songData = await (await fetch(trackEndpoint + trackId, options)).json(); 
    const analysisData = await (await fetch(analysisEndpoint + trackId, options)).json();


    console.log(trackId)
    // TODO: get artist id => get genre
}

async function fetchData(url, options) {
    return await (await fetch(url, options)).json();
} 

main()
