import network
import time
import socket
from machine import Pin
led = Pin(3, Pin.OUT)
state = 0
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>My Website</title>
    <style>
        #btn{
            height: 200px;
            width: 200px;
        }
    </style>
</head>
<body>
    <main>
        <button id="btn"> Turn %s</button>
    </main>
    <script>
        state = %s
        document.getElementById("btn").addEventListener("click", () => {
            fetch('http://176.115.8.105:54321', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "id": 78912 })
            })
            document.getElementById("btn").textContent = "Turn " + !state;
            state = !state
        });
    </script>
</body>
</html>
""" %(state, state)
def connect_wlan(ssid, passwd):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, passwd)

    maxWait = 10
    while maxWait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        maxWait -= 1
        print("waiting")
        time.sleep(1)
    if wlan.status() != 3:
        raise RuntimeError("network connection failed")
    else:
        print("connected")
        status = wlan.ifconfig()
        print("ip = ", status[0], " ", status)
    return wlan
wlan = connect_wlan("RMBnet_EXT", "md1104500")
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.1.129', 54321))
s.listen()
while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = str(request)
    print(request)
    if request.find("78912") > 0:
        led.toggle()
        state = not state
        
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send(html)
    conn.close()
