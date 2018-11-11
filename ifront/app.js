const express = require('express');

const app = express();

const http = require('http').Server(app)

app.use('/', express.static(__dirname + '/public'));


app.get('/api/get/all', (req, res) => {
    res.send(birth).end()
});


app.get('*', (req, res) => {
    res.status(404).end();
});

app.listen(3333, () => {
    console.log('localhost:80 에서 실행중');
});
