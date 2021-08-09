from sqlalchemy import Column, Integer, String, create_engine, Boolean, Table, ForeignKey
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///data.db')
Base = declarative_base()

basadoHecho = Table('basadoshechos',
                    Base.metadata,
                    Column("user", Integer, ForeignKey("users.id")),
                    Column("pariente", Integer, ForeignKey("parientebasados.id"))
)



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    basados = Column(Integer, default=0)
    basadosHechos = relationship("parientebasados", secondary=basadoHecho, backref=backref("basadoPorUsuarios", lazy ="dynamic"))
    parientesCreados = relationship("ParienteBasado", backref="autor")
    pildoras = relationship("Pildora", backref="recibidor")

    def __repr__(self) -> str:
        return f"User(username={self.username}, basados={self.basados})"

class ParienteBasado(Base):
    __tablename__ = "parientebasados"
    id = Column(Integer, primary_key=True)
    parentId = Column(String(9), unique=True, nullable=False)
    submissionId = Column(String(6), nullable=False)
    isComment = Column(Boolean, nullable=False)
    autorId = Column(Integer, ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"ParienteBasado(parentId={self.parentId}, submissionId={self.submissionId} isComment={self.isComment})"

class Pildora(Base):
    __tablename__ = "pildoras"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    ownerPildora = Column(Integer, ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"Pildora(name={self.name})"

sessionClass = sessionmaker(engine)
session = sessionClass()