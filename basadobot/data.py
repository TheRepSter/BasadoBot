import basadobot
from dataclasses import dataclass
from basadobot.models import User, Pildora
from praw.models import Submission, Comment

@dataclass
class reciber:
    recibidor : User
    comment : Submission or Comment
    pill : Pildora or None
