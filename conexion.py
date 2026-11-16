import psycopg2

def conectar():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            port="5432",
            database="acl_prototipo",
            user="postgres",
            password="132002"
        )

        return conexion

    except psycopg2.Error as error:
        print("Error de conexión:", error)
        return None