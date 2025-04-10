import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:3001'); // Connecte-toi au serveur

function App() {
    const [board, setBoard] = useState(Array(9).fill(null));
    const [isXNext, setIsXNext] = useState(true);
    const [gameOver, setGameOver] = useState(false);

    // Fonction pour vérifier si quelqu'un a gagné
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
        for (let i = 0; i < lines.length; i++) {
            const [a, b, c] = lines[i];
            if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
                return squares[a];
            }
        }
        return null;
    };

    // Gérer un clic sur une case
    const handleClick = (index) => {
        if (gameOver || board[index]) return;
        const newBoard = board.slice();
        newBoard[index] = isXNext ? 'X' : 'O';
        setBoard(newBoard);
        setIsXNext(!isXNext);
        
        const winner = calculateWinner(newBoard);
        if (winner) {
            setGameOver(true);
            alert(`${winner} a gagné !`);
        }
        socket.emit('move', { index, player: isXNext ? 'X' : 'O' });
    };

    useEffect(() => {
        socket.on('move', (data) => {
            const newBoard = board.slice();
            newBoard[data.index] = data.player;
            setBoard(newBoard);
        });
    }, [board]);

    return (
        <div>
            <h1>Jeu du Morpion</h1>
            <div className="board">
                {board.map((square, index) => (
                    <button
                        key={index}
                        className="square"
                        onClick={() => handleClick(index)}
                    >
                        {square}
                    </button>
                ))}
            </div>
            <p>{isXNext ? "C'est au tour de X" : "C'est au tour de O"}</p>
        </div>
    );
}

export default App;
