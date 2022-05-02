from pkg_resources import require
import telegram
import random
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import sqlite3
import math
import time
import asyncio
import json


from telegram.parsemode import ParseMode
from bot_modulo_salidas import *
from bot_modulo_calculate import *
from objeto_class import Objeto

# TOKEN EXTRACTION

token_file = open("auth.json")
token_value = json.loads(token_file.read().__str__())
token_value_str = token_value["token"].__str__()
print("BOT TOKEN = "+token_value_str)
token_file.close()

updater = Updater(token=token_value_str, use_context=True)
dispatcher = updater.dispatcher
job_queue = updater.job_queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# OBJETOS LOOTER CONTROLLERS #

def generar_loot_controller():

    loot = ""

    numero_aleatorio = random.randint(0,1000)

    if numero_aleatorio <= 350:
        loot += "mora"

    elif numero_aleatorio in range(351, 600):
        loot += "mid_weapon"

    elif numero_aleatorio in range(600, 820):
        loot += "mid_level"

    elif numero_aleatorio in range(820, 1000):
        loot += "primogem"

    return loot

def generar_cantidad_loot_controller(loot):

    cantidad = 0

    if loot == "mora":
        cantidad += random.randint(1500,5000)
    elif loot == "mid_weapon":
        cantidad += random.randint(8,15)
    elif loot == "mid_level":
        cantidad += random.randint(3,6)
    elif loot == "primogem":
        cantidad += random.choice([40,50,60])

    return cantidad

def usuario_en_cooldown_controller(id_usuario):

    respuesta = False

    tiempo = comprobar_tiempo_cooldown_bbdd(id_usuario)

    if int(time.time()) - tiempo <= 600:
        respuesta = True

    return respuesta



# GACHA PERSONAJES CONTROLLERS #

def tirar_al_gacha_controller():

    loot = ""

    numero_aleatorio = random.randint(0,1000)

    if numero_aleatorio <= 850:
        loot += "mora"

    elif numero_aleatorio <= 990:
        loot += "epico"

    else:
        loot += "legendario"

    return loot

def tiene_cantidad_objeto_controller(id_usuario, objeto, cantidad_necesaria):

    respuesta = False

    try:
        cantidad = comprobar_cantidad_objeto_bbdd(id_usuario, objeto)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
    else: pass

    respuesta = cantidad >= cantidad_necesaria

    return respuesta



# FORJA CONTROLLERS #

def cristales_forja_controller(id_usuario, operacion):

    respuesta = False
    cantidad_necesaria = 0
    objeto_a_forjar = ""
    cantidad_objeto_a_forjar = 0

    try:
        cantidad = comprobar_cantidad_objeto_bbdd(id_usuario, 'mid_weapon')
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
    else: pass

    # A PARTIR DE AQUÍ SE PUEDEN AÑADIR MÁS COSAS A LA FORJA

    if operacion == "primogem":
        cantidad_necesaria = 100
        cantidad_objeto_a_forjar = 60
        objeto_a_forjar += "primogem"



    # ---------------------------------------------------- #

    if cantidad >= cantidad_necesaria:
        respuesta = True
        
    return respuesta, cantidad_necesaria, objeto_a_forjar, cantidad_objeto_a_forjar

# TIENDA CONTROLLERS #

def tienda_controller(id_usuario, nombre_objeto):

    dinero_usuario = 0

    objeto_a_comprar = Objeto("",nombre_objeto,0,"")

    try:
        comprobar_cantidad_objeto_bbdd(id_usuario, 'mora')   
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
    else: pass

    



## BASES DE DATOS REGISTRAR USUARIO ##

def registrar_usuario_bbdd(id_usuario, usuario): 

    time_data = int(time.time())-600

    # time_forja_data = int(time.time())-3600

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute("INSERT INTO USUARIOS VALUES (?,?,?)", (id_usuario, usuario, time_data))

    conexion_bbdd.commit()

    conexion_bbdd.close()

def generar_inventario_nuevo_usuario_bbdd(id_usuario, usuario):

    tupla_de_objetos = ((id_usuario, usuario, 'mora', 0),(id_usuario, usuario, 'mid_weapon', 0),(id_usuario, usuario, 'mid_level', 0),(id_usuario, usuario, 'primogem', 0))

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.executemany(f"INSERT INTO USUARIOS_OBJETOS_OBTENIDOS VALUES (?,?,?,?)", tupla_de_objetos)

    conexion_bbdd.commit()

    conexion_bbdd.close()

def generar_inventario_personajes_usuario_bbdd(id_usuario, usuario):

    tupla_de_personajes = ((id_usuario, usuario, 'amber', 0, 'epico'),(id_usuario, usuario, 'barbara', 0, 'epico'),(id_usuario, usuario, 'beidou', 0, 'epico'),(id_usuario, usuario, 'bennet', 0, 'epico'),
                        (id_usuario, usuario, 'chongyun', 0, 'epico'),(id_usuario, usuario, 'diluc', 0, 'legendario'),(id_usuario, usuario, 'fischl', 0, 'epico'),(id_usuario, usuario, 'jean', 0, 'legendario'),
                        (id_usuario, usuario, 'kaeya', 0, 'epico'),(id_usuario, usuario, 'keqing', 0, 'legendario'),(id_usuario, usuario, 'klee', 0, 'legendario'),(id_usuario, usuario, 'lisa', 0, 'epico'),
                        (id_usuario, usuario, 'mona', 0, 'legendario'),(id_usuario, usuario, 'ningguang', 0, 'epico'),(id_usuario, usuario, 'noelle', 0, 'epico'),(id_usuario, usuario, 'qiqi', 0, 'legendario'),
                        (id_usuario, usuario, 'razor', 0, 'epico'),(id_usuario, usuario, 'sucrose', 0, 'epico'),(id_usuario, usuario, 'venti', 0, 'legendario'),(id_usuario, usuario, 'xiangling', 0, 'epico'),
                        (id_usuario, usuario, 'xiao', 0, 'legendario'),(id_usuario, usuario, 'xingqiu', 0, 'epico'),(id_usuario, usuario, 'tartaglia', 0, 'legendario'),(id_usuario, usuario, 'zhongli', 0, 'legendario'),
                        (id_usuario, usuario, 'xinyan', 0, 'epico'),(id_usuario, usuario, 'ganyu', 0, 'legendario'),(id_usuario, usuario, 'albedo', 0, 'legendario'),(id_usuario, usuario, 'diona', 0, 'epico'),
                        (id_usuario, usuario, 'rosaria', 0, 'epico'),(id_usuario, usuario, 'kamisato_ayaka', 0, 'legendario'),(id_usuario, usuario, 'yanfei', 0, 'epico'),(id_usuario, usuario, 'hu_tao', 0, 'legendario'),
                        (id_usuario, usuario, 'eula', 0, 'legendario'),(id_usuario, usuario, 'kaedehara_kazuha', 0, 'legendario'),(id_usuario, usuario, 'yoimiya', 0, 'legendario'),(id_usuario, usuario, 'sayu', 0, 'epico'),
                        (id_usuario, usuario, 'raiden_shogun', 0, 'legendario'),(id_usuario, usuario, 'sangonomiya_kokomi', 0, 'legendario'),(id_usuario, usuario, 'kujou_sara', 0, 'epico'),(id_usuario, usuario, 'aloy', 0, 'legendario'))

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.executemany("INSERT INTO USUARIOS_PERSONAJES_OBTENIDOS VALUES (?,?,?,?,?)", tupla_de_personajes)

    conexion_bbdd.commit()

    conexion_bbdd.close()



## BASES DE DATOS OBJETOS ##

def obtener_id_objeto(nombre_objeto):

    id_objeto = ""

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")
    
    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute(f"SELECT ID_OBJETO FROM OBJETOS WHERE NOMBRE_OBJETO = ?", (nombre_objeto,))

    id_objeto = cursor_bbdd.fetchall()[0][0]

    conexion_bbdd.close()

    return id_objeto

def ver_lista_de_objetos():

    lista_de_objetos = []

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute("SELECT NOMBRE_OBJETO FROM OBJETOS")

    lista_de_objetos = cursor_bbdd.fetchall()

    conexion_bbdd.close()

    return lista_de_objetos

def revisar_inventario_bbdd(id_usuario):

    lista_de_objetos = {}

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute(f"SELECT NOMBRE_OBJETO, CANTIDAD_OBJETO FROM USUARIOS_OBJETOS_OBTENIDOS WHERE ID_USUARIO = ?", (id_usuario,))

    tupla_de_objetos = cursor_bbdd.fetchall()

    lista_de_objetos = dict(tupla_de_objetos)

    conexion_bbdd.close()

    return lista_de_objetos

def obtener_info_objeto_bbdd(nombre_objeto):

    descripcion_objeto = ""

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")
    
    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute(f"SELECT DESCRIPCION_OBJETO FROM OBJETOS WHERE NOMBRE_OBJETO = ?", (nombre_objeto,))

    descripcion_objeto += cursor_bbdd.fetchall()[0][0]

    conexion_bbdd.close()

    return descripcion_objeto


## BASES DE DATOS TRANSACCIONES CON OBJETOS ##

def comprobar_cantidad_objeto_bbdd(id_usuario, objeto):

    cantidad = 0

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute(f"SELECT CANTIDAD_OBJETO FROM USUARIOS_OBJETOS_OBTENIDOS WHERE ID_USUARIO = ? AND NOMBRE_OBJETO = ?", (id_usuario, objeto))

    resultado_query = cursor_bbdd.fetchall()
    
    cantidad = int(resultado_query[0][0])

    conexion_bbdd.close()

    return cantidad

def agregar_objeto_a_usuario_bbdd(id_usuario, objeto, nueva_cantidad):

    cantidad_total = 0

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute(f"SELECT CANTIDAD_OBJETO FROM USUARIOS_OBJETOS_OBTENIDOS WHERE ID_USUARIO = ? AND NOMBRE_OBJETO = ?", (id_usuario, objeto))

    antigua_cantidad = cursor_bbdd.fetchall()[0][0]

    cantidad_total = antigua_cantidad + nueva_cantidad

    cursor_bbdd.execute(f"UPDATE USUARIOS_OBJETOS_OBTENIDOS SET CANTIDAD_OBJETO = ? WHERE ID_USUARIO = ? AND NOMBRE_OBJETO = ?", (cantidad_total, id_usuario, objeto))
            
    conexion_bbdd.commit()

    conexion_bbdd.close()

def cobrar_objeto_a_usuario_bbdd(id_usuario, objeto, cantidad_a_cobrar):

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute("SELECT CANTIDAD_OBJETO FROM USUARIOS_OBJETOS_OBTENIDOS WHERE ID_USUARIO = ? AND NOMBRE_OBJETO = ?", (id_usuario, objeto))

    cantidad_actual = cursor_bbdd.fetchall()[0][0]

    nueva_cantidad = int(cantidad_actual) - cantidad_a_cobrar

    cursor_bbdd.execute(f"UPDATE USUARIOS_OBJETOS_OBTENIDOS SET CANTIDAD_OBJETO = ? WHERE ID_USUARIO = ? AND NOMBRE_OBJETO = ?", (nueva_cantidad, id_usuario, objeto))

    conexion_bbdd.commit()

    conexion_bbdd.close()



## BASES DE DATOS LOOTER ##

def sumar_tiempo_cooldown_usuario_bbdd(id_usuario):

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    nuevo_tiempo = int(time.time())

    cursor_bbdd.execute(f"UPDATE USUARIOS SET TIME = ? WHERE ID_USUARIO = ?", (nuevo_tiempo, id_usuario))

    conexion_bbdd.commit()

    conexion_bbdd.close()

def comprobar_tiempo_cooldown_bbdd(id_usuario):

    tiempo = 0

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute(f"SELECT TIME FROM USUARIOS WHERE ID_USUARIO = ?", (id_usuario,))

    resultado_query = cursor_bbdd.fetchall()
    
    tiempo = int(resultado_query[0][0])

    conexion_bbdd.close()

    return tiempo



## BASES DE DATOS GACHA PERSONAJES ##

def sacar_personaje_aleatorio_bbdd(rareza):

    personaje = ""
    
    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute(f"SELECT NOMBRE_PERSONAJE FROM PERSONAJES WHERE RAREZA_PERSONAJE = ?", (rareza,))

    lista_personajes = cursor_bbdd.fetchall()

    personaje = random.choice(lista_personajes)[0]

    conexion_bbdd.close()

    return personaje

def agregar_personaje_a_usuario_bbdd(id_usuario, personaje):

    cantidad_total = 0

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute(f"SELECT CANTIDAD_PERSONAJE FROM USUARIOS_PERSONAJES_OBTENIDOS WHERE ID_USUARIO = ? AND NOMBRE_PERSONAJE = ?", (id_usuario, personaje))

    antigua_cantidad = cursor_bbdd.fetchall()[0][0]

    cantidad_total = antigua_cantidad + 1

    cursor_bbdd.execute(f"UPDATE USUARIOS_PERSONAJES_OBTENIDOS SET CANTIDAD_PERSONAJE = ? WHERE ID_USUARIO = ? AND NOMBRE_PERSONAJE = ?", (cantidad_total, id_usuario, personaje))
            
    conexion_bbdd.commit()

    conexion_bbdd.close()

def listar_personajes_bbdd():
    
    lista_de_personajes = []

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute("SELECT NOMBRE_PERSONAJE FROM PERSONAJES")

    lista_de_personajes = cursor_bbdd.fetchall()

    conexion_bbdd.close()

    return lista_de_personajes

def comprobar_inventario_personajes_bbdd(id_usuario):

    cantidad_necesaria = 1

    inventario_de_personajes = []

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cantidad_necesaria = 1

    cursor_bbdd.execute(f"SELECT NOMBRE_PERSONAJE, CANTIDAD_PERSONAJE FROM USUARIOS_PERSONAJES_OBTENIDOS WHERE ID_USUARIO = ? AND CANTIDAD_PERSONAJE >= ?", (id_usuario, cantidad_necesaria))

    inventario_de_personajes = dict(cursor_bbdd.fetchall())

    conexion_bbdd.close()

    return inventario_de_personajes

def ver_personaje_bbdd(personaje):

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute(f"SELECT NOMBRE_PERSONAJE, RAREZA_PERSONAJE, ELEMENTO_PERSONAJE, TIPO_ARMA_PERSONAJE FROM PERSONAJES WHERE NOMBRE_PERSONAJE = ?", (personaje,))

    datos_personaje = cursor_bbdd.fetchall()

    conexion_bbdd.close()

    return datos_personaje



## BASES DE DATOS FORJA ##

# Iniciar timer de forjado de objeto (id_usuario, tiempo) // Void

# def iniciar_temporizador_forja_bbdd(id_usuario):

#     conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

#     cursor_bbdd = conexion_bbdd.cursor()

#     tiempo_inicio_forja = int(time.time())

#     cursor_bbdd.execute(f"UPDATE USUARIO SET TEMPORIZADOR_FORJA = {tiempo_inicio_forja} WHERE ID_USUARIO = {id_usuario}")

#     conexion_bbdd.commit()

#     conexion_bbdd.close()



## BASES DE DATOS TIENDA ##



def comprobar_temporizador_forja_bbdd(id_usuario):

    respuesta = False

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute(f"SELECT TEMPORIZADOR_FORJA FROM USUARIOS WHERE ID_USUARIO = ?", (id_usuario,))

    tiempo_anterior = cursor_bbdd.fetchall()[0][0]

    tiempo_actual = int(time.time())

    diferencia_tiempo = tiempo_actual - int(tiempo_anterior)

    if diferencia_tiempo >= 3600:
        respuesta = True

    conexion_bbdd.close()

    return respuesta, diferencia_tiempo



###  GENSHIN REGISTRAR USUARIO HANDLER ###

def registrar_usuario(update, context):

    id_usuario = update.message.from_user.id
    usuario = update.message.from_user.username
    
    print(id_usuario)

    try:
        usuario_existente = registrar_usuario_bbdd(id_usuario, usuario)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: usuario {usuario} ya existe o no se ha podido acceder correctamente a la base de datos.")
    else:
        if usuario_existente:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"No se ha completado el registro porque ya existe un usuario <i>{usuario}</i> en la base de datos.", parse_mode=telegram.ParseMode.HTML)
        else:

            try:
                generar_inventario_nuevo_usuario_bbdd(id_usuario, usuario)
            except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print("Exception class is: ", er.__class__)
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: el usuario {usuario} fue registrado pero hubo un problema al generar su inventario. ERROR_INVENTARIO_OBJETOS")
            else: pass

            try:
                generar_inventario_personajes_usuario_bbdd(id_usuario, usuario)
            except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print("Exception class is: ", er.__class__)
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: el usuario {usuario} fue registrado pero hubo un problema al generar su inventario. ERROR_INVENTARIO_PERSONAJES")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Usuario: <i>{usuario}</i> registrado correctamente.", parse_mode=telegram.ParseMode.HTML)
            

registrar_usuario_handler = CommandHandler('registrarme', registrar_usuario)
dispatcher.add_handler(registrar_usuario_handler)



###  GENSHIN LOOTEAR OBJETO HANDLER ###

def lootear_objeto(update, context):

    id_usuario = update.message.from_user.id

    if not usuario_en_cooldown_controller(id_usuario):

        objeto = generar_loot_controller()
        cantidad = generar_cantidad_loot_controller(objeto)

        try:
            agregar_objeto_a_usuario_bbdd(id_usuario, objeto, cantidad)
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Ha habido un error accediendo a la base de datos. ERROR_AGREGAR_OBJETO")
        else:
            context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=open(f'genshin_prizes/{objeto}.png', 'rb'))
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"<b>Obtenido: {cantidad} <i>{objeto.capitalize()}</i></b>.", parse_mode=telegram.ParseMode.HTML)

            ### DESHABILITADO PARA FACILITAR TESTING
            #
            # try:
            #     sumar_tiempo_cooldown_usuario_bbdd(id_usuario)
            # except sqlite3.Error as er:
            #     print('SQLite error: %s' % (' '.join(er.args)))
            #     print("Exception class is: ", er.__class__)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Lo siento, pero tienes ese comando en cooldown.")

lootear_objeto_handler = CommandHandler('lootear', lootear_objeto)
dispatcher.add_handler(lootear_objeto_handler)

def revisar_inventario(update, context):

    id_usuario = update.message.from_user.id

    inventario = {}
    message = ""

    try:
        inventario = revisar_inventario_bbdd(id_usuario)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Error al acceder a la lista.")
    else:
        for i in inventario:
            message += f"<b>- {i} * {inventario[i]}\n\n</b>"
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=telegram.ParseMode.HTML)

revisar_inventario_handler = CommandHandler('mi_inventario', revisar_inventario)
dispatcher.add_handler(revisar_inventario_handler)

def listar_objetos(update, context):
    lista_de_objetos = []
    message = ""

    try:
        lista_de_objetos = ver_lista_de_objetos()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Error al acceder a la lista.")
    else:
        for i in lista_de_objetos:
            message += f"<b>- {i[0]} \n\n</b>"
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=telegram.ParseMode.HTML)

listar_objetos_handler = CommandHandler('listar_objetos', listar_objetos)
dispatcher.add_handler(listar_objetos_handler)



### GACHA PERSONAJES HANDLERS ###

def tirar_gacha(update, context):

    id_usuario = update.message.from_user.id

    if tiene_cantidad_objeto_controller(id_usuario, 'primogem', 80):

        resultado = tirar_al_gacha_controller()

        if resultado == "mora":
            objeto = resultado
            cantidad = random.randint(40000, 80000)

            try:
                cobrar_objeto_a_usuario_bbdd(id_usuario, 'primogem', 80)
            except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print("Exception class is: ", er.__class__)
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos. ERROR_COBRAR_GEMAS")
            else:
                try:
                    agregar_objeto_a_usuario_bbdd(id_usuario, objeto, cantidad)
                except sqlite3.Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print("Exception class is: ", er.__class__)
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos. ERROR_AGERGAR_MORA")

                    try:
                        agregar_objeto_a_usuario_bbdd(id_usuario, 'primogem', 80)
                    except sqlite3.Error as er:
                        print('SQLite error: %s' % (' '.join(er.args)))
                        print("Exception class is: ", er.__class__)
                        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos. ERROR_DEVOLVER_GEMAS")
                    else:
                        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Se han devuelto las primogems utilizadas en la última tirada.")

                else:
                    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=open(f'genshin_prizes/{objeto}.png', 'rb'))
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"<b>Su premio es: {cantidad} <i>{objeto.capitalize()}</i></b>. Más suerte la próxima vez.", parse_mode=telegram.ParseMode.HTML)
            
        else:
            rareza = resultado

            try:
                personaje = sacar_personaje_aleatorio_bbdd(rareza)
            except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print("Exception class is: ", er.__class__)
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos. ERROR_GENERAR_PERSONAJE")
            else:

                try:
                    cobrar_objeto_a_usuario_bbdd(id_usuario, 'primogem', 80)
                except sqlite3.Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print("Exception class is: ", er.__class__)
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos. ERROR_COBRAR_GEMAS")
                else:

                    try:
                        agregar_personaje_a_usuario_bbdd(id_usuario, personaje)
                    except sqlite3.Error as er:
                        print('SQLite error: %s' % (' '.join(er.args)))
                        print("Exception class is: ", er.__class__)
                        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos. ERROR_AGREGAR_PERSONAJE")

                        try:
                            agregar_objeto_a_usuario_bbdd(id_usuario, 'primogem', 80)
                        except sqlite3.Error as er:
                            print('SQLite error: %s' % (' '.join(er.args)))
                            print("Exception class is: ", er.__class__)
                            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos. ERROR_DEVOLVER_GEMAS")
                        else:
                            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Se han devuelto las primogems utilizadas en la última tirada.")

                    else:
                        nombre_personaje = personaje.replace("_"," ")
                        if rareza == "epico":
                            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f'genshin_characters/{personaje}/{personaje}_gacha_splash.png', 'rb'), caption=f"<b>¡Genial! ¡El personaje épico {nombre_personaje.capitalize()}</b> se ha unido a tu equipo!.", parse_mode=telegram.ParseMode.HTML)
                        elif rareza == "legendario":
                            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f'genshin_characters/{personaje}/{personaje}_gacha_splash.png', 'rb'), caption=f"<b>¡Felicidades! ¡El personaje legendario {nombre_personaje.capitalize()}</b> se ha unido a tu equipo!.", parse_mode=telegram.ParseMode.HTML)


    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Lo siento, pero no tienes suficientes <b>primogems</b>. Necesitas al menos <b>80</b> para hacer una tirada.", parse_mode=telegram.ParseMode.HTML)


tirar_gacha_handler = CommandHandler('gachapon', tirar_gacha)
dispatcher.add_handler(tirar_gacha_handler)

def listar_personajes(update, context):

    mensaje = ""

    try:
        lista_personajes = listar_personajes_bbdd()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos.")
    else:
        for i in lista_personajes:
            mensaje += f"<b>- {i[0]}</b>.\n"
        mensaje = mensaje.replace("_", " ").title()
        context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje, parse_mode=telegram.ParseMode.HTML)

listar_personajes_handler = CommandHandler('personajes', listar_personajes)
dispatcher.add_handler(listar_personajes_handler)

def comprobar_inventario_personajes(update, context):

    id_usuario = update.message.from_user.id

    mensaje = ""

    try:
        inventario = comprobar_inventario_personajes_bbdd(id_usuario)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos.")
    else:
        for i in inventario:
            mensaje += f"<b>- {i} * {inventario[i]}\n</b>"
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje, parse_mode=telegram.ParseMode.HTML)

comprobar_inventario_personajes_handler = CommandHandler('mis_personajes', comprobar_inventario_personajes)
dispatcher.add_handler(comprobar_inventario_personajes_handler)

def ver_personaje(update, context):

    personaje = ' '.join(context.args)
    personaje_a_buscar = personaje.lower()

    if len(context.args) == 1:
        try:
            datos_personaje = ver_personaje_bbdd(personaje_a_buscar)
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos.")
        else:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f'genshin_characters/{personaje}/{personaje}.png', 'rb'), caption=f"Nombre:  <b>{datos_personaje[0][0].capitalize()}</b>.\nRareza:  <b>{datos_personaje[0][1].capitalize()}</b>.\nElemento:  <b>{datos_personaje[0][2].capitalize()}</b>.\nArma:  <b>{datos_personaje[0][3].capitalize()}</b>.", parse_mode=telegram.ParseMode.HTML)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Nombre de Personaje no válido.")

    
ver_personaje_handler = CommandHandler('ver_personaje', ver_personaje)
dispatcher.add_handler(ver_personaje_handler)


### FORJA HANDLERS ###

def forjar_objeto(update, context):

    id_usuario = update.message.from_user.id

    operacion = ' '.join(context.args).lower()

    # try:
    #     forja_disponible, diferencia_tiempo = comprobar_temporizador_forja_bbdd(id_usuario)
    # except sqlite3.Error as er:
    #     print('SQLite error: %s' % (' '.join(er.args)))
    #     print("Exception class is: ", er.__class__)
    #     context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos. ERROR_ACCESO_TEMPORIZADOR")
    # else: pass

    # if forja_disponible:

    tiene_cristales, cobro, objeto, cantidad_objeto_a_forjar = cristales_forja_controller(id_usuario, operacion)

    if context.args:

        if tiene_cristales:

            try:
                cobrar_objeto_a_usuario_bbdd(id_usuario, 'mid_weapon', cobro)
            except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print("Exception class is: ", er.__class__)
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos. ERROR_COBRAR_CRISTALES")
            else:
                # iniciar_temporizador_forja_bbdd(id_usuario)
                try:
                    agregar_objeto_a_usuario_bbdd(id_usuario, objeto, cantidad_objeto_a_forjar)
                except sqlite3.Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print("Exception class is: ", er.__class__)
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos. ERROR_AGREGAR_GEMAS")

                    try:
                        agregar_objeto_a_usuario_bbdd(id_usuario, 'mid_weapon', cobro)
                    except sqlite3.Error as er:
                        print('SQLite error: %s' % (' '.join(er.args)))
                        print("Exception class is: ", er.__class__)
                        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error accediendo a la base de datos. ERROR_DEVOLVER_CRISTALES_FORJA")

                else:
                    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=open(f'genshin_prizes/{objeto}.png', 'rb'))
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Forjado: {cantidad_objeto_a_forjar} <b>{objeto.capitalize()}</b>.", parse_mode=telegram.ParseMode.HTML)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"No tienes suficientes cristales para forjar este objeto.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Argumento no válido. Por favor, especifica el objeto que quieres forjar como argumento tal y como está nombrado en la lista de objetos. Ver: [/listar_objetos]")
    # else:
        # context.bot.send_message(chat_id=update.effective_chat.id, text=f"Tu forja está ocupada actualmente. Inténtalo de nuevo en {diferencia_tiempo/60} minuto(s)")

forjar_objeto_handler = CommandHandler('forjar', forjar_objeto)
dispatcher.add_handler(forjar_objeto_handler)

### SALIDAS HANDLERS ###

crear_salida_handler = CommandHandler('crear_salida', crear_salida)
dispatcher.add_handler(crear_salida_handler)

confirmar_salida_handler = CommandHandler('confirmar_asistencia', confirmar_salida)
dispatcher.add_handler(confirmar_salida_handler)

revisar_salidas_handler = CommandHandler('revisar_salidas', revisar_salidas)
dispatcher.add_handler(revisar_salidas_handler)
    


### START HANDLER ###

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy la bot Elissabeth, aunque puedes llamarme Eliss. ¡Encantada!")

start_handler = CommandHandler('saludo', start)
dispatcher.add_handler(start_handler)



### SAY HANDLER ###

def say(update, context):
    final_text = ' '.join(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=final_text)

echo_handler = CommandHandler('decir', say)
dispatcher.add_handler(echo_handler)



### CALCULATE HANDLER ###

calculate_handler = CommandHandler('calcular', calculate)
dispatcher.add_handler(calculate_handler)



### CAPS HANDLER ###

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

caps_handler = CommandHandler('mayus', caps)
dispatcher.add_handler(caps_handler)



### HELP COMMAND HANDLER ###

def help(update, context):

    help_message = f""" <b>MENÚ DE AYUDA</b> \n
     - <b>/ayuda</b> => Despliega este menú de ayuda.\n
     - <b>/saludo</b> =>  Hace que Eliss salude en el chat.\n
     - <b>/decir</b> => El bot repetirá el mensaje que le indiques tras este comando. Ej: [/decir Mañana quiero carne asada].\n
     - <b>/mayus</b> => Hace lo mismo que /decir pero transforma todo el texto en mayúsculas.\n
     - <b>/calcular</b> => Hace un cálculo sencillo. Ej: [/calcular 43 + 21]. Ej2: [/calcular sqrt 144]. Soporta suma(+), resta(-), multiplicación(*), división(/), potencia(pow) y raíz cuadrada(sqrt)\n
     - <b>/registrarme</b> => Registra al usuario en el sistema del Juego Gacha basado en Genshin de Eliss.\n
     - <b>/lootear</b> => Permite sacar un objeto aleatorio de la lista de posibles objetos. Este comando tiene un cooldown de 10 minutos.\n
     - <b>/listar_objetos</b> => Permite ver la lista de objetos disponibles para sacar con el comando /lootear.\n
     - <b>/mi_inventario</b> => Permite al usuario revisar su inventario de objetos recibidos a lo largo del tiempo.\n
     - <b>/crear_salida</b> => Se creará una salida. Se pueden especificar detalles en su nombre como argumento de este comando. Ej: [/crear_salida Salida del Viernes por la tarde].\n
     - <b>/confirmar_asistencia</b> => El usuario confirmará su asistencia a una salida existente, la cual deberá especificar introduciendo su ID (ver /revisar_salidas para más información) como argumento. Ej: [/confirmar_asistencia 3].\n
     - <b>/revisar_salidas</b> => Permite ver la lista de salidas disponibles, así como el ID de las mismas para confirmar la asistencia con /confirmar_asistencia a la salida deseada.\n
     - <b>/gachapon</b> => El usuario realiza una tirada al Gacha. Puede tocar una cantidad de Mora, un Personaje Épico o uno Legendario. Se requieren 80 primogems para tirar, que serán deducidas del total del usuario tras la obtención de cualquier recompensa.\n
     - <b>/personajes</b> => Permite ver la lista total de personajes disponibles.\n
     - <b>/mis_personajes</b> => Permite al usuario ver su inventario de personajes.\n
     - <b>/ver_personaje</b> => Permite al usuario ver información sobre un personaje en concreto de la lista total de personajes. Ej: [/ver_personaje sangonomiya_kokomi].\n
     - <b>/forjar</b> => [/forjar *args] - WIP -
    """
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message, parse_mode=telegram.ParseMode.HTML)

help_handler = CommandHandler('ayuda', help)
dispatcher.add_handler(help_handler)



### UNKNOWN COMMAND HANDLER ###

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="No entiendo lo que me has dicho, quizás no es un comando.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)



### START ###

updater.start_polling()

updater.idle()