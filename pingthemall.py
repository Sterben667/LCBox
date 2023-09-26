from ping3 import ping 
from threading import Thread
import psutil 
import colorama
import ipaddress
import subprocess
import re
from time import sleep 

ip_up = []
interface_reseau : list
masque_de_sous_reseau : str
c : str

def get_netmask_of_interfaces(ip_addrs): 
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        for addr in addrs:
            if ip_addrs == addr.address:
                return addr.netmask
    return None
            

def list_network_interfaces():
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        print(f"{interface}")
        for addr in addrs:
            print(f"  {addr.family.name} Address: {addr.address}")
            if addr.netmask != None:
                print(f"  Masque de sous réseau : {addr.netmask}")
            

def ping_host(host, queue, retries=3, delay=1):
    """
    Cette fonction pinge une adresse IP et met le résultat dans une queue.
    :param host: L'adresse IP à ping.
    :param queue: La queue où mettre le résultat.
    :param retries: Nombre de fois à essayer le ping.
    :param delay: Temps à attendre entre les essais en secondes.
    """
    for i in range(retries):
        try:
            response_time = ping(host, timeout=4)  # Assurez-vous que la fonction 'ping' prend en charge le paramètre 'timeout'
            if response_time is not False:
                queue.put((host, True))
                return
        except Exception as e:
            print(f"Erreur lors du ping de {host}: {e}")

        if i < retries - 1:
            sleep(delay)

    queue.put((host, False))



def get_mac_address(ip_address):
    try:
        # Exécute la commande ARP pour récupérer l'adresse MAC associée à l'adresse IP donnée
        output = subprocess.check_output(["arp", "-n", ip_address]).decode("utf-8")
        
        # Utiliser une expression régulière pour extraire l'adresse MAC
        match = re.search(r"(([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2}))", output)
        
        if match:
            return match.group(0)
        else:
            return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération de l'adresse MAC pour {ip_address}: {e}")
        return None
