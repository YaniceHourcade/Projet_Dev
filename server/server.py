import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 5000

waiting_queue = []
games = {}

def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # lignes
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # colonnes
        [0, 4, 8], [2, 4, 6]  # diagonales
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
            return board[combo[0]]  # Retourne le joueur gagnant ('X' ou 'O')

    if " " not in board:  # égalité
        return "draw"

    return None  # Pas de gagnant, la partie continue

def handle_client(conn, addr):
    print(f"[+] Nouveau client : {addr}")

    try:
        data = conn.recv(1024).decode()
        msg = json.loads(data)

        if msg['action'] == 'enqueue':
            pseudo = msg['pseudo']
            ip, port = addr

            # Ajouter à la file d'attente
            waiting_queue.append({
                'conn': conn,
                'pseudo': pseudo,
                'ip': ip,
                'port': port
            })
            print(f"Ajouté à la file d’attente : {pseudo} ({ip}:{port})")

            # Vérification de la file d'attente pour créer un match
            if len(waiting_queue) >= 2:
                player1 = waiting_queue.pop(0)
                player2 = waiting_queue.pop(0)

                # Plateau vide
                empty_board = [" " for _ in range(9)]

                # Sauvegarder les infos du match
                game_id = len(games) + 1  # ID du match
                games[game_id] = {
                    'players': [player1, player2],
                    'board': empty_board,
                    'turn': 0,  # Le joueur 1 commence
                    'game_id': game_id
                }

                # Envoyer le début de match aux joueurs
                start_msg_p1 = {
                    "action": "start",
                    "role": "X",
                    "opponent": player2['pseudo'],
                    "board": empty_board
                }

                start_msg_p2 = {
                    "action": "start",
                    "role": "O",
                    "opponent": player1['pseudo'],
                    "board": empty_board
                }

                player1['conn'].send(json.dumps(start_msg_p1).encode())
                player2['conn'].send(json.dumps(start_msg_p2).encode())
                print(f"Match entre {player1['pseudo']} et {player2['pseudo']} démarré.")

                # Envoi de la première mise à jour à player1 (car c'est son tour)
                update_msg = {
                    "action": "update",
                    "your_turn": True,
                    "board": empty_board
                }
                player1['conn'].send(json.dumps(update_msg).encode())

        elif msg['action'] == 'play':
            game = games.get(msg['game_id'])
            if game:
                current_player = game['players'][game['turn']]
                opponent_player = game['players'][1 - game['turn']]
                board = game['board']

                # Appliquer le coup
                case = msg['case']
                if board[case] == " ":
                    board[case] = "X" if game['turn'] == 0 else "O"

                    # Vérifier s'il y a un gagnant
                    result = check_winner(board)
                    if result:
                        end_msg = {
                            "action": "end",
                            "result": "draw" if result == "draw" else f"{result} wins",
                            "board": board
                        }
                        current_player['conn'].send(json.dumps(end_msg).encode())
                        opponent_player['conn'].send(json.dumps(end_msg).encode())
                        del games[msg['game_id']]  # Supprimer le match après la fin
                    else:
                        # Changer le tour et envoyer l'update
                        game['turn'] = 1 - game['turn']
                        update_msg = {
                            "action": "update",
                            "your_turn": game['turn'] == 0,
                            "board": board
                        }
                        current_player['conn'].send(json.dumps(update_msg).encode())
                        opponent_player['conn'].send(json.dumps(update_msg).encode())

    except Exception as e:
        print(f"[!] Erreur : {e}")
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[🟢] Serveur lancé sur {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
