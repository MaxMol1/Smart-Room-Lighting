const fetch = require("node-fetch");
const cheerio = require('cheerio')
const Genius = require('genius-api');

async function Main() {
    /* Function to get artist id */
    Genius.prototype.getArtistID = async function getArtistID(artistName) {
        const response = await this.search(artistName)
        for (let i = 0; i < response.hits.length; i += 1) {
            const hit = response.hits[i]
            if (hit.type === 'song' && normalizeName(hit.result.primary_artist.name) === artistName)
                return hit.result.primary_artist.id
        }
        throw new Error("Did not find an artist called: " + artistName)
    }
    
    /* Function to get song page HTML */
    Genius.prototype.getSongHTML = async function getSongHTML(geniusUrl) {
        const response = await fetch(geniusUrl, { method: 'GET' })
        if (response.ok) {
            return await response.text()
        } else {
            console.log('Invalid song url...')
            exit()
        }
    }

    /* Function to parse lyrics from HTML */
    async function parseSongHTML(htmlText) {
        const $ = cheerio.load(htmlText)
        return $('.lyrics').text()
    }

    // genius access token
    const accessToken = 'XfpcBSGdEivzTpfOBtxy6hwKgBLFOYRb5Zla2UADZp9MVVV3xBsTFZ9FUK1wwv3q'
    const genius = new Genius(accessToken)
    
    // artist and song for which to find lyrics
    const normalizeName = name => name.replace(/[^\w]/g, '').toLowerCase()
    const song_name = normalizeName(process.argv[2])
    const artist_name = normalizeName(process.argv[3])

    /* 1. Get artist ID using artist name */
    const artistID = await genius.getArtistID(artist_name)

    /* 2. Get top 50 songs by artist */
    const songs = await genius.songsByArtist(artistID, {
        per_page: 50,
        sort: 'popularity'
    })

    /* 3. Get correct song url from list of 50 songs  */
    let songUrl
    songs.songs.some(song => {
        const title = song.title
        if (normalizeName(title) === song_name) {
            songUrl = song.url
            return
        }
    })

    /* 4. Fetch and parse html from song url */
    const songHTML = await genius.getSongHTML(songUrl)
    var lyrics = await parseSongHTML(songHTML)

    /* 5. Return lyrics to console */
    console.log(lyrics)
}

Main().catch(console.error)
