import sqlite3
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

## BASES DE DATOS SALIDAS ##

def introducir_salidas_bbdd(datos_salida):

    conexion_bbdd = sqlite3.connect("bot_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute("INSERT INTO SALIDAS VALUES (NULL,?,?)", datos_salida)

    conexion_bbdd.commit()

    conexion_bbdd.close()


def actualizar_salidas_bbdd(usuario, id_salida):

    success = False

    conexion_bbdd = sqlite3.connect("bot_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute(f"SELECT LISTA_USUARIOS FROM SALIDAS WHERE ID = {id_salida}")

    resultado_query = cursor_bbdd.fetchall()

    lista_usuarios = resultado_query[0][0]

    if usuario in lista_usuarios:

        print(f"USUARIO {usuario} YA REGISTRADO. NO SE HA REALIZADO EL UPDATE.")

    else:

        lista_usuarios += f", {usuario}"

        cursor_bbdd.execute("UPDATE SALIDAS SET LISTA_USUARIOS = ? WHERE ID = ?", (lista_usuarios, id_salida))

        conexion_bbdd.commit()

        print(f"USUARIO {usuario} REGISTRADO CORRECTAMENTE.")

        success = True
    
    conexion_bbdd.close()

    return success


def obtener_salidas_bbdd():

    conexion_bbdd = sqlite3.connect("bot_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.execute("SELECT * FROM SALIDAS")

    lista_salidas = cursor_bbdd.fetchall()

    conexion_bbdd.close()

    return lista_salidas



### HANDLERS SALIDAS ###

def crear_salida(update, context):

    datos_salida = []
    info_salida = ' '.join(context.args)
    usuario = update.message.from_user.username

    datos_salida.append(info_salida)
    datos_salida.append(usuario)

    try:
        introducir_salidas_bbdd(datos_salida)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha ocurrido un error en la base de datos al crear la salida.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Su salida se ha creado satisfactoriamente.")

def confirmar_salida(update, context):

    id_salida = ' '.join(context.args)
    usuario = update.message.from_user.username

    try:
        success = actualizar_salidas_bbdd(usuario, id_salida)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ha habido un error al intentar confirmar su asistencia a la salida.")
    else:

        if success:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"El usuario {usuario} ha confirmado su asistencia a la próxima salida.")

        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"El usuario {usuario} ya está registrado en la salida, por lo que no se ha incluído de nuevo.")

def revisar_salidas(update, context):

    salida = obtener_salidas_bbdd()

    print(salida)

    output = ""

    for elemento in salida:
        output += f"<b>Salida Nº {elemento[0]}</b>. <i>{elemento[1].__str__()}</i>. <b>Asistentes: </b><i>{elemento[2].__str__()}</i>.\n\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{output}", parse_mode=telegram.ParseMode.HTML)
