#python version=3.13.12
import socket
import threading
import random
from time import sleep

#=================================#
#             config              #
#=================================#
SERVER_IP='192.168.1.197'#IPv4
SERVER_PORT=8888
moves=["scissors","rock","paper"]
#=================================#

#parameter:player_move
#return:server_result,player_result,server_move
#pending for result
def winning_pending(player_move:str):
    server_move=random.randint(0,2)
    player_move=moves.index(player_move)
    results={0:"Draw", 1:"Win", 2:"Lose"}
    return results[(server_move-player_move)%3],results[(player_move-server_move)%3],moves[server_move] 
#target for threads(main logic)
def player_handler(connect:socket.socket,host_ip):
    wins=0
    print(f"New player joined, now serving {host_ip}")
    player_name=connect.recv(1024).decode("utf-8")
    connect.send(f"Welcome Game {player_name}".encode("utf-8"))
    connect.send("ALL_SENT".encode())
    while True:
        
        player_move=connect.recv(1024).decode("utf-8")
        server_result,player_result,server_move=winning_pending(player_move)
        if player_result == "Win": wins+=1
        #server output
        print(f"In competetion with {player_name}({host_ip}), Server {server_result}")
        #client output
        connect.send((f"Server move: {server_move}\n"+f"Result: {player_result}, Total wins: {wins}").encode("utf-8"))
        if wins!=3:connect.send("ALL_SENT".encode())
        if wins==3:
            connect.send("GAME_OVER".encode())
            connect.send("ALL_SENT".encode())
            break
    connect.send("You have winned 3 times, socket closing...".encode("utf-8"))
    connect.close()
    print(f"Socket with {host_ip} Finished")
    print("Closing threads...")

server=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server.bind((SERVER_IP,SERVER_PORT))
server.listen(2)
print("server opened successfully")
while True:
    conn=server.accept()
    #once player joined, new a thread just for him
    #thus support muti 1 to 1
    t=threading.Thread(target=player_handler,args=(conn[0],conn[1]))
    t.start()
    