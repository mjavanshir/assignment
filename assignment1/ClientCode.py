import socket

server_host = '127.0.0.1'  # IP سرور
server_port = 12345        # پورت اتصال

# ایجاد سوکت TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# اتصال به سرور
client_socket.connect((server_host, server_port))
print(f"اتصال به سرور {server_host}:{server_port} برقرار شد.")

try:
    while True:
        # ارسال پیام به سرور
        message = input("پیام خود را وارد کنید: ")
        client_socket.send(message.encode('utf-8'))
        if message.lower() == "exit":
            print("ارتباط توسط کلاینت بسته شد.")
            break

        # دریافت پاسخ از سرور
        data = client_socket.recv(1024).decode('utf-8')
        if not data or data.lower() == "exit":
            print("ارتباط توسط سرور بسته شد.")
            break
        print(f"سرور: {data}")
        
# بستن ارتباط       
finally:
    client_socket.close()
