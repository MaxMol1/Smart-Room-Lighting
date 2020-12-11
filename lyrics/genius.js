const fetch = require("node-fetch");
const cheerio = require('cheerio')
const Genius = require('genius-api');
const { exit } = require("process");

async function Main() {
    Genius.prototype.getSongUrl = async function getSongUrl(artistName, songName) {
        const normalizeName = name => name.replace(/[^\w]/g, '').toLowerCase()
        const artistNameNormalized = normalizeName(artistName)
        const songNameNormalized = normalizeName(songName)
    
        const response = await this.search(artistName)
        for (let i = 0; i < response.hits.length; i += 1) {
            const hit = response.hits[i]
            if (hit.type === 'song' && normalizeName(hit.result.primary_artist.name) === artistNameNormalized
               && normalizeName(hit.result.title) === songNameNormalized)
                    // Todo: buggy ..? why do I need this print
                    console.log('')
                    return hit.result.url
        }
        throw new Error("Did not find any songs whose artist is " + artistName)
    }
    
    Genius.prototype.getSongHTML = async function getSongHTML(geniusUrl) {
        const response = await fetch(geniusUrl, { method: 'GET' })
        if (response.ok) {
            return await response.text()
        } else {
            console.log('Invalid song url...')
            exit()
        }
    }

    async function parseSongHTML(htmlText) {
        const $ = cheerio.load(htmlText)
        return $('.lyrics').text()
    }

    // genius access token
    const accessToken = 'XfpcBSGdEivzTpfOBtxy6hwKgBLFOYRb5Zla2UADZp9MVVV3xBsTFZ9FUK1wwv3q'
    const genius = new Genius(accessToken)
    const artist_name = process.argv[3]
//    const artist_name = 'drake'
    const song_name = process.argv[2]
//    const song_name = 'timeflies'

    // Main routine
    const songUrl = await genius.getSongUrl(artist_name, song_name)
    const songHTML = await genius.getSongHTML(songUrl)
    var lyrics = await parseSongHTML(songHTML)

    console.log('~~~~ FETCHING LYRICS COMPLETE ~~~~')
    console.log(lyrics)

}
Main().catch(console.error)
