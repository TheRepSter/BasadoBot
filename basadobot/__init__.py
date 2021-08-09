from basadobot.models import User, ParienteBasado, Pildora, session
from basadobot.security import security
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

    def modificarBasados(self, basado):
        pariente = session.query(ParienteBasado).filter(ParienteBasado.parentId == basado.parent_id).first()
        if not pariente:
            if basado.parent_id[1] == 3:
                reci = self.reddit.comment(basado.parent_id).parent().author
            
            else:
                reci = basado.submission.author

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
        
        else:
            recibidor = session.query(User).filter(User.id == pariente.autorId)
        
        commenter = session.query(User).filter(User.username == basado.author.id).first()
        if not commenter:
            commenter = User(username = basado.author.id)
        
        commenter.basadosHechos.append(pariente)
        if security(commenter, pariente, recibidor):
            session.add(commenter)
            session.add(pariente)
            session.add(recibidor)

            return recibidor

    def commit_changes(self):
        print("Commited changes!")
        session.commit()

    def dar_pildoras(self, basado, recibidor):
        basadoNew, pillWord = basado 
        nombrePill = basadoNew.body.lower().split(pillWord)[0].split(" ")[-1]
        
        pill = Pildora(name=nombrePill, recibidor=recibidor)
        session.add(pill)
        return pill

    def mensaje_basado(self, recib):
        if recib.pill and recib.recibidor.basados in messages:
            message = f"""¡El usuario u/{recib.recibidor.username} ha conseguido una pildora y ha subido de nivel a la vez!
            
            La pildora es {recib.pill.name}.
            
            Ahora es nivel {recib.recibidor.basados}:{messages.get(recib.recibidor.basados)}

            Tiene las siguientes pildoras: {', '.join(list(map(lambda x: x.name, recib.recibidor.pildoras)))}

            ¿Alguna duda? ¡Hablame por MD!
            """
        elif recib.pill:
            num = recib.recibidor.basados
            nombre = messages.get(num)
            while not nombre:
                num -= 1
                nombre = messages.get(num)

            message = f"""¡El usuario u/{recib.recibidor.username} ha conseguido una pildora!
            
            La pildora es {recib.pill.name}.
            
            Él es de nivel {recib.recibidor.basados}:{nombre}
            
            Tiene las siguientes pildoras: {', '.join(list(map(lambda x: x.name, recib.recibidor.pildoras)))}

            ¿Alguna duda? ¡Hablame por MD!
            """

        elif recib.recibidor.basados in messages:
            message = f"""¡El usuario u/{recib.recibidor.username} ha subido de nivel!
            
            Ahora es nivel {recib.recibidor.basados}:{messages.get(recib.recibidor.basados)}
            
            Tiene las siguientes pildoras: {', '.join(list(map(lambda x: x.name, recib.recibidor.pildoras)))}

            ¿Alguna duda? ¡Hablame por MD!
            """
            if isinstance(recib.comment, Comment):
                recib.comment.reply(message)
            else:
                recib.comment.add_comment(message)

        
    def comprovar_mensaje(self, receb) -> bool:
        return receb.pill or receb.recibidor.basados in messages

    def mirar_basados(self) -> list:
        nuevosBasados = []

        subreddit_inspection = self.reddit.subreddit("BasadoBot")

        for comment in subreddit_inspection.comments(limit=100):
            palabraEncontrada = ""
            for palabra in ["basado", "based"]:
                if palabra in comment.body.lower()[:len(palabra)]:
                    palabraEncontrada = palabra
                    break
            
            else:
                continue
            
            pildora = ""
            for palabra in ["pileado", "pilleado", "pilled", "pildoreado"]:
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
                recibe = self.modificarBasados(basado[0])
                if not recibe:
                    continue
                pill = None
                if basado[1]:
                    pill = self.dar_pildoras(basado[0], basado[1])
                recibidores.append(reciber(recibe, basado[0], pill))

            self.commit_changes()
            for receb in recibidores:
                if self.comprovar_mensaje(receb):
                    sleep(1)
                    self.mensaje_basado(receb)

            sleep(10)