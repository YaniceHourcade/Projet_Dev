const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');

const app = express();
app.use(cors());

const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: 'http://localhost:3000',
        methods: ['GET', 'POST']
    }
});

let players = {};
let playerCount = 0;

app.get('/', (req, res) => {
    res.send('Serveur Morpion');
});

io.on('connection', (socket) => {
    console.log('Un utilisateur s\'est connecté');

    if (playerCount >= 2) {
        socket.emit('full');
        socket.disconnect();
        return;
    }

    const symbol = playerCount === 0 ? 'X' : 'O';
    players[socket.id] = symbol;
    playerCount++;

    socket.emit('playerSymbol', symbol);
    console.log(`Joueur ${symbol} connecté`);

    socket.on('move', (data) => {
        // Réémet à tous les joueurs (y compris l'envoyeur)
        io.emit('move', data);
    });

    socket.on('disconnect', () => {
        console.log(`Joueur ${players[socket.id]} déconnecté`);
        delete players[socket.id];
        playerCount--;
    });
});

server.listen(3001, () => {
    console.log('Le serveur écoute sur http://localhost:3001');
});
