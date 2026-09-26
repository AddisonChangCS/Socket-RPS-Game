#python version=3.13.12
import socket
import random

#=================================#
#             config              #
#=================================#
SERVER_IP='192.168.1.197'#IPv4
SERVER_PORT=8888
moves=["scissors","rock","paper"]
#=================================#
#              datas              #
#=================================#
players=[]
players.append({'name':"Server",'score':0,'socket':None})
all_moves=[]
#=================================#
def winning_pending():
    unique_set=set(all_moves)
    if len(unique_set)==2:
        m1, m2 = unique_set
        win_map = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
        winner_move = m1 if win_map[m1] == m2 else m2
        for i in range(3):
            if all_moves[i]==winner_move: players[i]['score']+=1
def output_str_generate():
    output =  f"{'Name':<8} | {'Score':>5}"
    output += f"\n{'-'*9}|{'-'*7}"
    for p in players:
        output+=f"\n{p['name']:<8} | {p['score']:>5}"
    return output

server=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server.bind((SERVER_IP,SERVER_PORT))
server.listen(2)
print("server opened successfully")
while len(players)<3:
    conn,ip=server.accept()
    print(f"New player joined, from IP {ip}")
    player_name=conn.recv(1024).decode("utf-8")
    conn.send(f"Welcome Game {player_name}".encode("utf-8"))
    players.append({'name':player_name,'score':0,'socket':conn})
    if len(players)<3:
        conn.send("Waiting for another person join...".encode())
players[1]['socket'].send("Game start!ALL_SENT".encode())
players[2]['socket'].send("Game start!ALL_SENT".encode())

for i in range(3):
    all_moves.clear()
    all_moves.append(random.choice(moves))
    all_moves.append(players[1]['socket'].recv(1024).decode())
    all_moves.append(players[2]['socket'].recv(1024).decode())

    print(f"{f'Round {i}':^21}\n" + "-"*21)
    for i in range(3):
        print(f"{players[i]['name']:^9} | {all_moves[i]:^9}")
    winning_pending()
    players[1]['socket'].send(output_str_generate().encode())
    players[2]['socket'].send(output_str_generate().encode())
    if i!=3:
        players[1]['socket'].send("ALL_SENT".encode())
        players[2]['socket'].send("ALL_SENT".encode())

players[1]['socket'].send("GAME_OVER".encode())
players[2]['socket'].send("GAME_OVER".encode())
players[1]['socket'].send("ALL_SENT".encode())
players[2]['socket'].send("ALL_SENT".encode())

print("socket closed successfully")

    
    