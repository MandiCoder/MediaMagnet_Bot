from time import time, localtime

sec = 0
# ===============================================================================# PROGRESS BAR


def text_progres(index, max):
    try:
        if max < 1:
            max += 1
        porcent = index / max
        porcent *= 100
        porcent = round(porcent)
        make_text = ""
        index_make = 1
        make_text += "\n__[__ "
        while index_make < 21:
            if porcent >= index_make * 5:
                make_text += "__▣__"
            else:
                make_text += "__□__"
            index_make += 1
        make_text += " __]__"
        return make_text
    except Exception as ex:
        return ""


def update_progress_bar(inte, max):
    percentage = inte / max
    percentage *= 100
    percentage = round(percentage)
    hashes = int(percentage / 5)
    spaces = 20 - hashes
    progress_bar = "[" + "■" * hashes + "□" * spaces + "]"
    percentage_pos = int(hashes / 1)
    percentage_string = "[" + str(percentage) + "%" + "]"
    progress_bar = (
        progress_bar[:percentage_pos]
        + percentage_string
        + progress_bar[percentage_pos + len(percentage_string) :]
    )
    return progress_bar


# ===============================================================================# PROGRESS DOWNLOAD


def progressddl(current, total, msg, start, rest=0):
    global sec
    act = time() - start
    speed = round((round(current / 1000000, 2) / act), 2)
    if sec != localtime().tm_sec:
        try:
            txt = f"**🚛 Descargando...\n{update_progress_bar(current, total)}"
            txt += f"\n\n📁 Archivos pendientes: {rest}"
            txt += f"\n📊 Total :{round(total/1000000,2)} MB"
            txt += f"\n📲 Descargado: {round(current/1000000,2)} MB"
            txt += f"\n🚀 Velocidad: {speed} MB/s**"
            msg.edit_text(txt)
        except:
            pass
    sec = localtime().tm_sec


# ===============================================================================# PROGRESS UPLOAD


async def progressupl(current, total, sms, totalFiles, count, start):
    global sec
    act = time() - start
    speed = round((round(current / 1000000, 2) / act), 2)
    if sec != localtime().tm_sec:
        try:
            await sms.edit_text(
                f"**📤 Subiendo: {count}-{totalFiles}\n__{update_progress_bar(current,total)}__\n🗄 Total :{round(total/1000000,2)} MB \n🗂 Subido: {round(current/1000000,2)}\n⚡️ Velocidad: {speed} MB/s**"
            )
        except:
            pass
    sec = localtime().tm_sec


# ===============================================================================# YOUTUBE PROGRESS


def progressytdl(current, total, speed, filename, tiempo, message, bots):
    # porcent = int(current * 100 / total)
    filename = filename.split("/")[-1]
    global sec
    if sec != localtime().tm_sec:
        try:
            text = f"📥 **Descargando**\n\n💾**Name**: {filename} \n"
            text += f"{update_progress_bar(current,total)}\n\n"
            text += f"🗄 **Total**:{round(total/1000000,2)} MiB \n"
            text += f"🗂 **Descargado**: {round(current/1000000,2)}MiB\n"
            text += f"⏱ **Tiempo**: {tiempo}\n"
            text += f"⚡️ **Velocidad: {round(current/1000000,2)} MB/s**"
            bots.edit_message_text(message.chat.id, message.id, text)
        except:
            pass
        sec = localtime().tm_sec


# ===============================================================================# TWITCH PROGRESS


def progresstwitch(current, speed, filename, tiempo, message, bots):
    filename = filename.split("\\")[-1]
    global sec
    if sec != localtime().tm_sec:
        try:
            text = f"📥 **Descargando\n\n💾Name: {filename} \n\n**"
            text += f"🗂 **Descargado: {round(current/1000000,2)}MB\n**"
            text += f"⚡️ **Velocidad: {round(float(speed)/1000000,2)} MB/s\n**"
            text += f"⏱ **Tiempo: {tiempo}\n**"
            bots.edit_message_text(message.chat.id, message.id, text)
        except:
            pass
        sec = localtime().tm_sec


# ===============================================================================# WGET PROGRESS


def progresswget(current, total, filename, start, message, bots):
    porcent = int(current * 100 // total)
    act = time() - start
    speed = round((round(current / 1000000, 2) / act), 2)
    global sec
    if sec != localtime().tm_sec:
        try:
            text = f"**📥 Descargando...**\n"
            text += f"__{update_progress_bar(current,total)} {speed} MB/s__\n\n"
            text += f"🗄 **Total**: {round(total/1000000,2)} MiB \n"
            text += f"🗂 **Descargado**: {round(current/1000000,2)}MiB\n"
            text += f"⚡️ **Velocidad: {speed} MB/s**"
            bots.edit_message_text(message.chat.id, message.id, text)
        except:
            pass
        sec = localtime().tm_sec
