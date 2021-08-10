from basadobot.models import User, ParienteBasado, Pildora, session
from basadobot.security import security1, security2
from basadobot.data import reciber
from praw.models import Comment
import praw
from time import sleep

#mensajes copiados de u/basedcount_bot momentaneamente
messages = {
            1:"Casa de cartas",
            5:"Árbol joven",
            10:"Silla de oficina",
            20:"Canasta de baloncesto (llena de arena)",
            35:"Luchador de sumo",
            50:"Fundación de hormigón",
            75:"Sequoia gigante",
            100:"Empire State Building",
            200:"Gran pirámide de Giza",
            350:"Edificio de ensamblaje de vehículos de la ESA",
            500:"Fábrica de Boeing Everett",
            750:"Monte Fuji", 
            1000:"Denali",
            2000:"Annapurna"}

class bot:
    def __init__(self, **kwargs):
        self.reddit = praw.Reddit(**kwargs)

    def dar_basado(self, basado):
        pariente = security2(basado)
        if pariente == None:
            reci = basado.parent().author
            recibidor = session.query(User).filter(User.username == str(reci)).first()
            
            if recibidor:
                recibidor.basados += 1

            else:
                recibidor = User(username=str(reci), basados=1)
            
            pariente = ParienteBasado(parentId = basado.parent_id,
                        submissionId = basado.link_id,
                        isComment = basado.parent_id[1] == 1,
                        autor = recibidor
            )
        
        elif pariente == False:
            return

        else:
            recibidor = session.query(User).filter(User.id == pariente.autorId).first()
        
        commenter = session.query(User).filter(User.username == str(basado.author)).first()
        if not commenter:
            commenter = User(username = str(basado.author))
        
        if security1(commenter, pariente, recibidor):
            commenter.basadosHechos.append(pariente)
            session.add(commenter)
            session.add(pariente)
            session.add(recibidor)

            return recibidor

    def commit_changes(self):
        print("Commited changes!")
        session.commit()

    def dar_pildoras(self, recibidor, basado, pillWord): 
        nombrePill = basado.body.lower().split(pillWord)[0].split(" ")[-1]
        
        pill = Pildora(name=nombrePill, recibidor=recibidor)
        session.add(pill)
        return pill

    def mensaje_basado(self, recib):
        if recib.pill != None and recib.recibidor.basados in messages:
            message = "\n\n".join([
                f"¡El usuario u/{recib.recibidor.username} ha conseguido una pildora y ha subido de nivel a la vez!",
                f"La píldora es {recib.pill.name}.",
                f"Ahora es nivel {recib.recibidor.basados}:{messages.get(recib.recibidor.basados)}",
                f"Tiene las siguientes píldoras: {', '.join(list(map(lambda x: x.name, recib.recibidor.pildoras)))}"
            ])

        elif recib.pill != None:
            num = recib.recibidor.basados
            nombre = messages.get(num)
            while not nombre:
                num -= 1
                nombre = messages.get(num)

            message = "\n\n".join([
                f"¡El usuario u/{recib.recibidor.username} ha conseguido una píldora!",
                f"La píldora es {recib.pill.name}.",
                f"Él es de nivel {recib.recibidor.basados}:{nombre}",
                f"Tiene las siguientes píldoras: {', '.join(list(map(lambda x: x.name, recib.recibidor.pildoras)))}"
            ])

        elif recib.recibidor.basados in messages:
            message = "\n\n".join([
                f"¡El usuario u/{recib.recibidor.username} ha subido de nivel!",
                f"Ahora es nivel {recib.recibidor.basados}:{messages.get(recib.recibidor.basados)}",
                f"Tiene las siguientes píldoras: {', '.join(list(map(lambda x: x.name, recib.recibidor.pildoras)))}"
            ])
            
        message += "\n\n¿Alguna duda? ¡Háblame por MD!"
        recib.comment.reply(message)

    def comprovar_mensaje(self, receb) -> bool:
        return receb.pill != None or receb.recibidor.basados in messages

    def mirar_basados(self) -> list:
        nuevosBasados = []

        subreddit_inspection = self.reddit.subreddit("BasadoBot")

        for comment in subreddit_inspection.comments(limit=100):
            palabraEncontrada = ""
            for palabra in ["basado", "basada", "based"]:
                if palabra in comment.body.lower()[:len(palabra)]:
                    palabraEncontrada = palabra
                    break
            
            else:
                continue
            
            pildora = ""
            for palabra in ["pileado", "pilleado", "pildoreado", "pileada", "pilleada", "pildoreada", "pilled"]:
                if palabra in comment.body.lower()[len(palabraEncontrada):]:
                    pildora = palabra
                    break
            
            nuevosBasados.append([comment, pildora])

        return nuevosBasados

    def run(self):
        while True:
            recibidores = []

            basadosActuales = self.mirar_basados()
            for basado in basadosActuales:
                recibe = self.dar_basado(basado[0])
                if not recibe:
                    continue

                pill = None
                if basado[1]:
                    pill = self.dar_pildoras(recibe, basado[0], basado[1])

                recibidores.append(reciber(recibe, basado[0], pill))

            if len(recibidores):
                self.commit_changes()

            for receb in recibidores:
                if self.comprovar_mensaje(receb):
                    sleep(1)
                    self.mensaje_basado(receb)

            sleep(10)