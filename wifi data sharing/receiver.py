import socket

HOST = "0.0.0.0"   # Listen on all interfaces
PORT = 5000

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((HOST, PORT))
server_sock.listen(1)

print("📡 Waiting for connection...")
print("💻 Receiver IP:", socket.gethostbyname(socket.gethostname()))
print(f"➡️ Listening on port {PORT}")

client_sock, addr = server_sock.accept()
print(f"✅ Connected from {addr}")

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print("📥 Received:", data.decode().strip())
except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")

client_sock.close()
server_sock.close()
