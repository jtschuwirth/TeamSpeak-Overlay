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
    return ",".join(msg)




def leer_mensajes():
    #file = "mensaje.txt"
    file =  "C:/Users/jtsch/OneDrive/Escritorio/Tibia/TS3/config/chats/dHo4TG5Zamx2WDFnaWhFSFAwallldVI5ajljPQ==/server.html"
    logfile = open(file, "r", encoding = "utf-8")
    loglines = follow(logfile)
    linea_anterior = ""
    sin_restriccion = False
    for line in loglines:
        if line.strip()=="":
            continue
        #Sin Restricciones
        if sin_restriccion == True:
            line = limpiar_mensaje(line)
            linea_anterior = line
            return line

        if "You were kicked from the server" in line:
            return ["", "TBot", "", "You were kicked from the server", "server", "serverlog"]
        elif "Disconnected from server" in line:
            return ["", "TBot", "", "Disconnected from the server", "server", "serverlog"]
        elif "Connected to Server:" in line:
            return ["", "TBot", "", "Connected to the server", "server", "serverlog"]
        else:
            continue
