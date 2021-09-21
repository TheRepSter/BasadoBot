from random import choice

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

def generador_frase(nombreuser):
    frase = choice(frases)
    if choice(range(25)) == 0:
        frase = frase.replace("{insertarnombre}", nombreuser)

    else:
        frase = frase.replace("{insertarnombre}", choice(nombres))
    
    frase = frase.replace("{nombreuser}", nombreuser)
    frase = frase.replace("{pais}", choice(paises))
    frase = frase.replace("{link}", choice(links))

    if frase[-1] not in [".", "?", "!"]:
        if frase[-1] == ",":
            frase[-1] == "."

        else:
            frase += "."

    if frase[-2] == ",":
        del frase[-2]

    return frase

def preguntaCunada():
    return choice(respuestaPregunta)

def messageCunado():
    return choice(respuestaResto)

def respuestaFeliz():
    return choice(["¡Gracias!", "¡Muchas gracias!", ":D", "¿Yo buen bot? ¡Tu eres un buen humano!"])
