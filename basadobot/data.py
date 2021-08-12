from dataclasses import dataclass
from basadobot.models import User, Pildora
from praw.models import Comment

#Clase para hacer más facil usar los datos, como un struct de C
@dataclass
class reciber:
    recibidor : User
    comment : Comment
    pill : Pildora or None
    def __repr__(self) -> str:
        return f"reciber(recibidor={repr(self.recibidor)}, comment={repr(self.comment)}, pill={repr(self.pill)})"