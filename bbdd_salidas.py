import sqlite3

def iniciar_bbdd():

    conexion_bbdd = sqlite3.connect("bot_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute('''
        
        CREATE TABLE SALIDAS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            INFO_SALIDA VARCHAR(255),
            LISTA_USUARIOS VARCHAR(255)
            )
        ''')

    conexion_bbdd.close()

iniciar_bbdd()