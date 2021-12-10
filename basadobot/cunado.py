from random import choice

fraseEvento = "\n\n¡Feliz Noche de las ánimas 2021! No te olvides de participar en [este](https://www.reddit.com/r/Asi_va_Espana/comments/q3bb58/extra_extra_spookctober_versi%C3%B3n_espa%C3%B1ita/) evento que está ocurriendo en el subreddit hasta el 31 de octubre a las 23:59"

def cargarLista(nombre : str):
    lista = []
    with open(f"utilsCunado/{nombre}.txt", encoding="UTF-8") as f:
        for i in f.read().splitlines():
            lista.append(i)

    return lista


respuestaPregunta = cargarLista("respuestaPregunta")
respuestaResto = cargarLista("respuestaResto")
paises  = cargarLista("paises")
frases  = cargarLista("frases")
nombres = cargarLista("nombres") + cargarLista("nombresSubreddit")
links   = cargarLista("links")
paraBasadoBot = cargarLista("respuestaBasadoBot")

def generador_frase(nombreuser):
    frase = choice(frases)
    if choice(range(25)) == 0:
        frase = frase.replace("{insertarnombre}", nombreuser)

    else:
        frase = frase.replace("{insertarnombre}", choice(nombres))
    
    frase = frase.replace("{nombreuser}", nombreuser)
    frase = frase.replace("{pais}", choice(paises))
    frase = frase.replace("{link}", choice(links))
    frase = frase.replace("{evento}", "")
    frase = frase.replace("{br}", "\n\n")
    frase = frase.strip()

    if frase[-1] not in [".", "?", "!"]:
        if frase[-1] == ",":
            frase[-1] == "."

        else:
            frase += "."

    if frase[-2] == ",":
        del frase[-2]

    return frase

def respuesta_basadobot_a_basadobot():
    frase = choice(paraBasadoBot)
    frase = frase.replace("{link}", choice(links))
    return frase

def preguntaCunada():
    return choice(respuestaPregunta)

def messageCunado():
    return choice(respuestaResto)

def respuestaFeliz():
    return choice(["¡Gracias!", "¡Muchas gracias!", ":D", "¿Yo buen bot? ¡Tu eres un buen humano!"])
