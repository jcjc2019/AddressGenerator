from multiprocessing.connection import Listener
from multiprocessing.connection import Client

receiving = True

# Receive data from Person generator
while receiving:
    listener = Listener(('localhost', 6000), authkey=b'success')
    conn = listener.accept()
    while True:
        msg = conn.recv()
        if msg == "close":
            conn.close()
            listener.close()
            # Send the data back to Person Generator
            connect = Client(('localhost', 6000), authkey=b'success')
            if connect:
                connect.send(data)
                connect.send('close')
                connect.close()
            else:
                print("Error occurred while connecting to Person Generator!")
            break
        else:
            data = str(msg)
            print(data)
