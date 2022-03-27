import time


def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def limpiar_mensaje(msg):
    msg = msg.replace("&quot;", "")
    msg = msg.replace("&nbsp;", " ")
    msg = msg.replace("&nbsp", " ")
    msg = msg.replace("&lt;", "")
    msg = msg.replace("&gt;", "")
    msg = msg.replace("&apos;","'")
    msg = msg.replace("&amp;","&")

    msg = msg.replace("Ã§", "ç")
    msg = msg.replace("Ã£", "ã")
    msg = msg.replace ("pokes you:", "")

    msg = [ x[:x.index("<")] if "<" in x else x for x in msg.split(">")]
    msg = map(lambda x: x.strip(" "), msg)
    msg = filter(lambda x: len(x) > 1, msg)
    msg = filter(lambda x: not(x[0] == "]" and x[-1] == "]"), msg)
    msg = map(lambda x: x[2:] if x[0] == "]" else x , msg)

    msg = [*msg]
    #msg[0] = Hora
    #msg[1] = quien envia el mensaje (TBot o persona)
    #msg[2] = si es por Tbot => quien lo mando o si murio alguien,en caso contrario es el mensaje
    #msg[3] = mensaje
    msg_limpio = []
    if msg[1] == "TBot": 
        if len(msg) == 3:
            #poke de informacion de Tbot
            msg_limpio = [msg[0], "TBot", "", msg[2]]
        elif len(msg) == 4:
            msg[2] = msg[2].strip(":")
            msg[2] = msg[2].strip(" ")
            msg[3] = msg[3].strip(":")
            msg[3] = msg[3].strip(" ")
            #arreglar mensaje cuando loga enemigo
            if "[" in msg[2] and "]" in msg[2]:
                msg_limpio = [msg[0], "TBot", "", ", ".join(msg[2:])]
            #poke normal 
            else:
                msg_limpio = [msg[0], "TBot", msg[2], msg[3]]
        else:
            #poke largos
            msg[2] = msg[2].strip(":")
            msg[2] = msg[2].strip(" ")
            msg[3] = msg[3].strip(":")
            msg[3] = msg[3].strip(" ")
            if "FRIENDS MATARAM" in msg[2]:
                msg_limpio = [msg[0], "TBot", "FRIENDS MATARAM", ", ".join(msg[3:])]
            elif "HUNTEDS MATARAM" in msg[2]:
                msg_limpio = [msg[0], "TBot", "HUNTEDS MATARAM", ", ".join(msg[3:])]
            elif "FRIEND MORREU" in msg[2]:
                msg_limpio = [msg[0], "TBot", "FRIEND MORREU", ", ".join(msg[3:])]
            elif "HUNTED MORREU" in msg[2]:
                msg_limpio = [msg[0], "TBot", "HUNTED MORREU", ", ".join(msg[3:])]
            else:
                msg_limpio = [msg[0], "TBot", msg[2], ", ".join(msg[3:])]

    else:
        #poke personal o mensaje por chat
        msg_limpio = [msg[0], "Pvt", msg[1], ", ".join(msg[2:])]

    if "shooter" in msg_limpio[3] or "Shooter" in msg_limpio[3] or "SHOOTER" in msg_limpio[3] or "shotter" in msg_limpio[3]:
        msg_limpio.append("bosses")
    elif "respawn" in msg_limpio[3]:
        msg_limpio.append("respawn")
    else:
        msg_limpio.append("normal")
    msg_limpio.append("chatlog")

    print(msg_limpio)
    print("")
    return msg_limpio

def leer_mensajes():
    #file = "mensaje.txt"
    file =  "C:/Users/jtsch/OneDrive/Escritorio/Tibia/TS3/config/chats/dHo4TG5Zamx2WDFnaWhFSFAwallldVI5ajljPQ==/channel.html"
    logfile = open(file, "r", encoding = "utf-8")
    loglines = follow(logfile)
    linea_anterior = ""
    for line in loglines:
        if line.strip()=="":
            continue
        #Quitar mensajes innecesarios
        elif "pokes you:" in line or "respawn" in line:
            if "FRIENDS MATARAM:" in line:
                continue
            elif "HUNTEDS MATARAM:" in line:
                continue
            elif "FRIEND MORREU:" in line:
                continue
            elif "HUNTED MORREU:" in line:
                continue
            
            line = limpiar_mensaje(line)
            #Quitar mensajes spameados
            if line == linea_anterior:
                continue
            linea_anterior = line
            return line
