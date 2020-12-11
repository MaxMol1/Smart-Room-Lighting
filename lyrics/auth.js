var express = require('express');

var app = express();
app.use(express.static(__dirname + '/public'))

app.set('port', process.env.PORT || 3000);

const CLIENT_ID = ''
const redirect_url = 'http://localhost:3000/'

app.get('/', function(req, res) {
  console.log('Hello World')
})

app.get('/login', function(req, res) {
  const scopes = 'user-read-private';
  const url = 'https://accounts.spotify.com/authorize' +
    '?response_type=code' +
    '&client_id=' + CLIENT_ID +
    (scopes ? '&scope=' + encodeURIComponent(scopes) : '') +
    '&redirect_uri=' + encodeURIComponent(redirect_url);
  res.redirect(url); 
});

console.log('Listening on 3000')
app.listen(3000);
