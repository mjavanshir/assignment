import socket

# تنظیمات سرور
server_host = '127.0.0.1'  # آدرس سرور
server_port = 12345        # پورت اتصال

# ایجاد سوکت TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# بایند کردن سوکت به آدرس و پورت
server_socket.bind((server_host, server_port))
# گوش دادن به اتصال‌ (حداکثر 1 اتصال در صف)
server_socket.listen(1)

print(f"منتظر اتصال کلاینت‌ بر روی پورت {server_port}...")


# پذیرش اتصال از کلاینت
client_socket, client_address = server_socket.accept()

#print(f"Connected by {client_address}")
print(f"اتصال برقرار شد از: {client_address}")


try:
    # دریافت و ارسال پیام‌ها
    while True:
          # دریافت پیام از کلاینت
        data = client_socket.recv(1024).decode('utf-8')
        if not data or data.lower() == "exit":
            # اگر کلاینت ارتباط را قطع کرد
            print("ارتباط توسط کلاینت بسته شد.")
            break
        print(f"کلاینت: {data}")
        
        # ارسال پاسخ به کلاینت
        message = input("پیام خود را وارد کنید: ") 
        client_socket.send(message.encode('utf-8')) 
        if message.lower() == "exit":
             print("ارتباط توسط سرور بسته شد.")
             break

finally:
    # بستن ارتباط
    client_socket.close()
    server_socket.close()


