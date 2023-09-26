class Machine:
    def __init__(self, ip_address, mac_address, open_ports=None):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.open_ports = open_ports  # Assumons que c'est une liste de ports ouverts

    def display_info(self):
        print(f"Adresse IP: {self.ip_address}")
        print(f"Adresse MAC: {self.mac_address}")
        print(f"Ports ouverts: {', '.join(map(str, self.open_ports))}")

