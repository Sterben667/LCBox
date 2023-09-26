import socket
import time
import mysql.connector
import threading
from ping3 import ping

ip_up = []

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password_here",
        database="network_scan"
    )
    
def insert_data(ip_address, port):
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO scan_results (ip_address, port) VALUES (%s, %s)"
    val = (ip_address, port)
    cursor.execute(sql, val)
    db.commit()
    db.close()
    
def ping_host(host):
    response_time = ping(host)
    if response_time is False:
        pass
    else:
        print(f"{host} à un temps de réponse de : {response_time}")
        ip_up.append(host)
    pass

def scan_port(ip_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip_address, port))
    if result == 0:
       return port

def scan_ports(ip_address, port_range):
    for port in port_range:
        thread = threading.Thread(target=scan_port, args=(ip_address, port))
        thread.start()
        

def scan_ips(ip_range, port_range):
    
    for ip in ip_range:
        scan_ports(ip, port_range)
        
        
