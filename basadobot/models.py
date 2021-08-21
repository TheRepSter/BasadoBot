from sqlalchemy import Column, Integer, String, create_engine, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///data.db')
Base = declarative_base()

class BasadoHecho(Base):
    __tablename__ = 'basadoshechos'
    user = Column(Integer, ForeignKey("users.id"), primary_key=True)
    pariente = Column(Integer, ForeignKey("parientebasados.id"), primary_key=True)

#Clase User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    basados = Column(Integer, default=0)
    basadosHechos = relationship("ParienteBasado", secondary="basadoshechos")
    parientesCreados = relationship("ParienteBasado", backref="autor")
    pildoras = relationship("Pildora", backref="recibidor")

    def __repr__(self) -> str:
        return f"User(username={self.username}, basados={self.basados})"

#Clase ParienteBasado
class ParienteBasado(Base):
    __tablename__ = "parientebasados"
    id = Column(Integer, primary_key=True)
    parentId = Column(String(9), unique=True, nullable=False)
    submissionId = Column(String(6), nullable=False)
    basadosHechos = relationship("User", secondary="basadoshechos")
    isComment = Column(Boolean, nullable=False)
    autorId = Column(Integer, ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"ParienteBasado(parentId={self.parentId}, submissionId={self.submissionId}, isComment={self.isComment})"

#Clase Pildora
class Pildora(Base):
    __tablename__ = "pildoras"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    ownerPildora = Column(Integer, ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"Pildora(name={self.name})"

#Clase OtherComment
class OtherComment(Base):
    __tablename__ = "othercomments"
    id = Column(Integer, primary_key=True)
    commentId = Column(String(7), unique=True, nullable=False)

sessionClass = sessionmaker(engine)
session = sessionClass()