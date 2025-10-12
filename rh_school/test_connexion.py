import psycopg2

try:
    conn = psycopg2.connect(
        dbname="gestion_rh",
        user="eva",
        password="isep",
        host="192.168.189.133",
        port="5432"
    )
    print("Connexion réussie !")
    conn.close()
except Exception as e:
    print("Erreur de connexion :", e)
