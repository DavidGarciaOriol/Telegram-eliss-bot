import sqlite3

def iniciar_bbdd_objetos():

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute('''
        CREATE TABLE OBJETOS(
            ID_OBJETO INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE_OBJETO VARCHAR(255)
        )
    ''')

    conexion_bbdd.close()

def iniciar_bbdd_usuarios():

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute('''
        CREATE TABLE USUARIOS(
            ID_USUARIO INTEGER PRIMARY KEY,
            NOMBRE_USUARIO VARCHAR(128),
            TIME INTEGER,
            TEMPORIZADOR_FORJA INTEGER,
            UNIQUE(NOMBRE_USUARIO, ID_USUARIO)
        )
    ''')

    conexion_bbdd.close()

def iniciar_bbdd_characters():

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute('''
            CREATE TABLE PERSONAJES(
                ID_PERSONAJE INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE_PERSONAJE VARCHAR(255),
                RAREZA_PERSONAJE VARCHAR(255),
                ELEMENTO_PERSONAJE VARCHAR(255),
                TIPO_ARMA_PERSONAJE VARCHAR(255)
            )
        ''')

    conexion_bbdd.close()

def iniciar_bbdd_users_objetos():

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute('''
        CREATE TABLE USUARIOS_OBJETOS_OBTENIDOS(
            ID_USUARIO INTEGER,
            NOMBRE_USUARIO VARCHAR(128),
            NOMBRE_OBJETO VARCHAR(255),
            CANTIDAD_OBJETO INTEGER,
            FOREIGN KEY(ID_USUARIO) REFERENCES USUARIOS(ID_USUARIO),
            FOREIGN KEY(NOMBRE_USUARIO) REFERENCES USUARIOS(NOMBRE_USUARIO),
            FOREIGN KEY(NOMBRE_OBJETO) REFERENCES OBJETOS(NOMBRE_OBJETO)
        )
    ''')
    conexion_bbdd.close()

def iniciar_bbdd_users_characters():

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute('''
            CREATE TABLE USUARIOS_PERSONAJES_OBTENIDOS(
                ID_USUARIO INTEGER,
                NOMBRE_USUARIO VARCHAR(128),
                NOMBRE_PERSONAJE VARCHAR(255),
                CANTIDAD_PERSONAJE INTEGER,
                RAREZA_PERSONAJE VARCHAR(255),
                FOREIGN KEY(ID_USUARIO) REFERENCES USUARIOS(ID_USUARIO),
                FOREIGN KEY(NOMBRE_USUARIO) REFERENCES USUARIOS(NOMBRE_USUARIO),
                FOREIGN KEY(NOMBRE_PERSONAJE) REFERENCES PERSONAJES(NOMBRE_PERSONAJE)
            )
        ''')

    conexion_bbdd.close()



# iniciar_bbdd_objetos()
# iniciar_bbdd_usuarios()
# iniciar_bbdd_characters()
# iniciar_bbdd_users_objetos()
# iniciar_bbdd_users_characters()