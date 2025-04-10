const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Définir la route de base
app.get('/', (req, res) => {
    res.send('Serveur Morpion');
});

// Gérer les événements de socket.io
io.on('connection', (socket) => {
    console.log('Un utilisateur s\'est connecté');
    socket.on('disconnect', () => {
        console.log('Un utilisateur s\'est déconnecté');
    });
});

server.listen(3001, () => {
    console.log('Le serveur écoute sur http://localhost:3001');
});
