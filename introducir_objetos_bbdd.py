import sqlite3

def introducir_objetos_bbdd(value):

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute('INSERT INTO OBJETOS VALUES (NULL,?)', (value,))

    conexion_bbdd.commit()

    conexion_bbdd.close()

introducir_objetos_bbdd("primogem")