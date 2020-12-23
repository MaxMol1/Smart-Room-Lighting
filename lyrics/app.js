var express = require('express');
const path = require('path');

/* Global Vars */
const CLIENT_ID = '';
const REDIRECT_URI = 'http://localhost:3000/main/';
const SCOPES = 'user-read-private'

var app = express();
app.set('port', process.env.PORT || 3000);

/* Auth/login endpoint */
app.get('/', function(req, res) {
  const url = 'https://accounts.spotify.com/authorize' +
    '?response_type=token' +
    '&client_id=' + CLIENT_ID +
    (SCOPES ? '&scope=' + encodeURIComponent(SCOPES) : '') +
    '&redirect_uri=' + encodeURIComponent(REDIRECT_URI);
  res.redirect(url); 
})

/* Callback endpoint */
app.get('/main', function(req, res) {
  res.sendFile(path.join(__dirname + '/public/index.html'));
})

/* Use static html,css,js files */
app.use('/js', express.static(__dirname + '/public/js'));

/* Listen on port 3000 */
app.listen(3000,()=>{
  console.log('Listening on port 3000...')
})
