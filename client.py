#python version=3.13.12
import socket
import threading

#=================================#
#             config              #
#=================================#
SERVER_IP='192.168.1.197'#IPv4
SERVER_PORT=8888
moves=["scissors","rock","paper"]
#=================================#
connect_state=False
name=""
start_signal = threading.Event()
def server_listener(connect:socket.socket):
    global connect_state
    global name
    while True:
        try:
            data=connect.recv(1024).decode("utf-8")
            if 'GAME_OVER' in data: 
                connect_state=False
                data=data.replace("GAME_OVER", "")
            if 'ALL_SENT' in data:
                start_signal.set()
                data=data.replace("ALL_SENT", "")
            if data!="":
                print(data)
        except:
            break
    
client=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
try:
    client.connect((SERVER_IP,SERVER_PORT))
    connect_state=True
    print("Connect success!")
    t=threading.Thread(target=server_listener,args=(client,))
    t.start()
    print("Please enter your name: ")
    name=input().strip()
    try:
        client.send(name.encode("utf-8"))
        #wait for all player
        start_signal.wait()
        start_signal.clear()
    except:
        print("something wrong with Server, sending error")
    while connect_state:
        print("Please enter your move(scissors,rock,paper): ")
        move=input().strip()
        if move in moves:
            try:
                client.send(move.encode("utf-8"))
                #wait for all player
                start_signal.wait()
                start_signal.clear()
            except:
                print("something wrong with Server, sending error")
        else:
            print("(!)Please enter CORRECT move(scissors,rock,paper)")
except ConnectionRefusedError:
    print("Server is down, try again...")
finally:
    print("connect close.")
    client.close()