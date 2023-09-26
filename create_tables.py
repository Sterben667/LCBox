import mysql.connector

# Fonction pour créer les tables dans la base de données MariaDB
def create_database_tables():
    try:
        # Établir une connexion à la base de données (remplacez les valeurs par les vôtres)
        conn = mysql.connector.connect(
            host="localhost",
            user="votre_utilisateur",
            password="votre_mot_de_passe",
            database="votre_base_de_donnees"
        )

        # Créer une instance du curseur
        cursor = conn.cursor()

        # Définir les requêtes SQL pour créer les tables
        create_informations_reseau_table = """
        CREATE TABLE IF NOT EXISTS informations_reseau (
            id INT AUTO_INCREMENT PRIMARY KEY,
            adresse_ip VARCHAR(15) NOT NULL,
            adresse_mac VARCHAR(17) NOT NULL,
            port VARCHAR(255)
        )
        """

        create_adb_ip_addresses_table = """
        CREATE TABLE IF NOT EXISTS adb_ip_addresses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ip_adress VARCHAR(15) NOT NULL
        )
        """

        # Exécuter les requêtes pour créer les tables
        cursor.execute(create_informations_reseau_table)
        cursor.execute(create_adb_ip_addresses_table)

        # Valider les changements dans la base de données
        conn.commit()

        # Fermer la connexion
        cursor.close()
        conn.close()

        print("Les tables ont été créées avec succès dans la base de données MariaDB.")

    except mysql.connector.Error as err:
        print(f"Erreur lors de la création des tables : {err}")

# Appeler la fonction pour créer les tables
create_database_tables()
