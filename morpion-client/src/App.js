import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:3001');

function App() {
    const [board, setBoard] = useState(Array(9).fill(null));
    const [isMyTurn, setIsMyTurn] = useState(false);
    const [mySymbol, setMySymbol] = useState(null);
    const [gameOver, setGameOver] = useState(false);
    const [status, setStatus] = useState("En attente d'un autre joueur...");

    const calculateWinner = (squares) => {
        const lines = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ];
        for (let [a, b, c] of lines) {
            if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
                return squares[a];
            }
        }
        return null;
    };

    const handleClick = (index) => {
        if (!isMyTurn || board[index] || gameOver) return;

        socket.emit('move', {
            index,
            player: mySymbol
        });
    };

    useEffect(() => {
        socket.on('playerSymbol', (symbol) => {
            setMySymbol(symbol);
            setIsMyTurn(symbol === 'X'); // X commence
            setStatus(`Tu es le joueur ${symbol}`);
        });

        socket.on('move', ({ index, player }) => {
            setBoard(prev => {
                const updated = [...prev];
                updated[index] = player;
                const winner = calculateWinner(updated);
                if (winner) {
                    setGameOver(true);
                    setStatus(`${winner} a gagné !`);
                } else if (!updated.includes(null)) {
                    setGameOver(true);
                    setStatus('Match nul !');
                } else {
                    setStatus(`C'est au tour de ${player === 'X' ? 'O' : 'X'}`);
                    setIsMyTurn(player !== mySymbol);
                }
                return updated;
            });
        });

        socket.on('full', () => {
            alert('La partie est déjà pleine !');
        });

        return () => {
            socket.off('playerSymbol');
            socket.off('move');
            socket.off('full');
        };
    }, [mySymbol]);

    return (
        <div>
            <h1>Jeu du Morpion</h1>
            <p>{status}</p>
            <div className="board" style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 100px)',
                gridGap: '10px',
                margin: '20px auto',
                width: 'max-content'
            }}>
                {board.map((square, index) => (
                    <button
                        key={index}
                        className="square"
                        onClick={() => handleClick(index)}
                        style={{
                            width: '100px',
                            height: '100px',
                            fontSize: '2rem',
                            cursor: 'pointer'
                        }}
                    >
                        {square}
                    </button>
                ))}
            </div>
        </div>
    );
}

export default App;
