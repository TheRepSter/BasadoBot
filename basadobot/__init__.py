from praw.reddit import Submission
from basadobot.models import User, ParienteBasado, Pildora, session, Base, engine
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
        basado = basado[0]
        pariente = session.query(ParienteBasado).filter(ParienteBasado.parentId == basado.parent_id).first()
        if not pariente:
            if basado.parentId[1] == 1:
                reci = self.reddit.comment(basado.parent_id).author
            
            else:
                reci = self.reddit.submission(basado.parent_id).author

            recibidor = session.query(User).filter(User.username == reci)
            
            if recibidor:
                recibidor.basados += 1

            else:
                recibidor = User(username=reci, basados=1)
            
            pariente = ParienteBasado(parentId = basado.parentId,
                        submissionId = basado.link_id,
                        isComment = basado.parentId[1] == 1,
                        autor = recibidor
            )
        
        else:
            recibidor = session.query(User).filter(User.id == pariente.autorId)
        
        commenter = session.query(User).filter(User.username == basado.author.id)
        if not commenter:
            commenter = User(username = basado.author.id)
        
        commenter.basadosHechos.append(pariente)
        session.add(commenter)
        session.add(pariente)
        session.add(recibidor)

        return recibidor

    def commit_changes(self):
        session.commit()

    def dar_pildoras(self, basado, recibidor):
        basadoNew, pillWord = basado 
        nombrePill = basadoNew.body.lower().split(pillWord)[0].split(" ")[-1]
        
        pill = Pildora(name=nombrePill, recibidor=recibidor)
        session.add(pill)

    def mensaje_basado(self):
        pass # TODO: Enviar mensaje a los que suben de nivel
    
    def comprovar_mensaje(self, basado) -> bool:
        return basado[1][1] or basado[0].basados in messages

    def mirar_basados(self) -> list:
        nuevosBasados = []

        subreddit_inspection = self.reddit.subreddit("Asi_va_Espana")

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
        recibidores = []

        basadosActuales = self.mirar_basados()
        for basado in basadosActuales:
            recibidores.append(self.modificarBasados(basado), basado)
            if basado[1]:
                self.dar_pildoras(basado, recibidores[-1])

        session.commit()
        for receb in recibidores:
            if self.comprovar_mensaje(receb):
                self.mensaje_basado()
