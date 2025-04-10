import socket
import json
import threading

HOST = '127.0.0.1'
PORT = 5000

# Stockage du socket pour envoyer les coups
global_sock = None
my_role = None
current_board = []

def listen_server(sock):
    global current_board, my_role

    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break

            msg = json.loads(data)

            if msg['action'] == 'start':
                print("\n🎮 Match trouvé !")
                print(f"Adversaire : {msg['opponent']}")
                my_role = msg['role']
                current_board = msg['board']
                print_board(current_board)

                # Demander au joueur de jouer
                ask_move()

            elif msg['action'] == 'update':
                print(f"\n🔄 Mise à jour du plateau")
                current_board = msg['board']
                print_board(current_board)

                if msg['your_turn']:
                    ask_move()

            elif msg['action'] == 'end':
                print("\n🏁 Fin du match")
                print(f"Résultat : {msg['result']}")
                current_board = msg['board']
                print_board(current_board)
                break

        except Exception as e:
            print(f"[!] Erreur de réception : {e}")
            break

def ask_move():
    while True:
        try:
            if my_role == 'X':  # Si c'est à toi de jouer
                case = int(input("🧠 Choisis une case (0-8) : "))
                if 0 <= case <= 8 and current_board[case] == " ":
                    msg = {
                        "action": "play",
                        "case": case
                    }
                    global_sock.send(json.dumps(msg).encode())
                    break
                else:
                    print("❌ Case invalide ou déjà prise.")
            else:
                print("🕒 Ce n'est pas encore ton tour...")
                break
        except ValueError:
            print("❌ Merci d’entrer un chiffre entre 0 et 8.")

def print_board(board):
    print("\n    0   1   2")
    print("  ┌───┬───┬───┐")
    for i in range(0, 9, 3):
        print(f"{i//3} │ {board[i]} │ {board[i+1]} │ {board[i+2]} │")
        if i < 6:
            print("  ├───┼───┼───┤")
    print("  └───┴───┴───┘")

def main():
    global global_sock
    pseudo = input("Entre ton pseudo : ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    global_sock = sock

    msg = {
        "action": "enqueue",
        "pseudo": pseudo
    }

    sock.send(json.dumps(msg).encode())
    print("🕒 En attente d'un adversaire...")

    threading.Thread(target=listen_server, args=(sock,), daemon=True).start()

    # Le programme reste vivant
    while True:
        pass

if __name__ == "__main__":
    main()
