from praw.reddit import Submission
from basadobot.models import User, ParienteBasado, session, Base, engine
import praw
from time import sleep

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

            recividor = session.query(User).filter(User.username == reci)
            
            if recividor:
                recividor.basados += 1
            else:
                recividor = User(username=reci, basados=1)
            pariente = ParienteBasado(parentId = basado.parentId,
                        submissionId = basado.link_id,
                        isComment = basado.parentId[1] == 1,
                        autor = recividor
            )
        else:
            recividor = session.query(User).filter(User.id == pariente.autorId)
        
        commenter = session.query(User).filter(User.username == basado.author.id)
        if not commenter:
            commenter = User(username = basado.author.id)
        commenter.basadosHechos.append(pariente)
        session.add(commenter)
        session.add(pariente)
        session.add(recividor)
    def mensaje_basado(self):
        pass # TODO: Enviar mensaje a los que suben de nivel
    
    def comprovar_nuevo_nivel(self):
        pass

    def sumar_basados(self, basado):
        pass

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
            pildora = False
            for palabra in ["pileado", "pilleado", "pilled"]:
                if palabra in comment.body.lower()[len(palabraEncontrada):]:
                    pildora = True
                    break
            nuevosBasados.append([comment, pildora])

        return nuevosBasados

    def run(self):
        basadosActuales = self.mirar_basados()
        for basado in basadosActuales:
            self.anadir_a_ids(basado)
        pass
