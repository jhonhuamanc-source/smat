<<<<<<< HEAD
<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class EstacionDB(Base):
    __tablename__ = "estaciones"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    ubicacion = Column(String)
    # Relación: permite acceder a las lecturas desde el objeto estación
    lecturas = relationship("LecturaDB", back_populates="estacion")

class LecturaDB(Base):
    __tablename__ = "lecturas"
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float)
    estacion_id = Column(Integer, ForeignKey("estaciones.id"))
    
    estacion = relationship("EstacionDB", back_populates="lecturas")
=======
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
class EstacionDB(Base):
    __tablename__ = "estaciones"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    ubicacion = Column(String)
    # Relación: permite acceder a las lecturas desde el objeto estación
    lecturas = relationship("LecturaDB", back_populates="estacion")

class LecturaDB(Base):
    __tablename__ = "lecturas"
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float)
    estacion_id = Column(Integer, ForeignKey("estaciones.id"))
    
    estacion = relationship("EstacionDB", back_populates="lecturas")
>>>>>>> 22179523fa1522c3e634baeda63fd0eb3f454aa9
=======
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
class EstacionDB(Base):
    __tablename__ = "estaciones"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    ubicacion = Column(String)
    # Relación: permite acceder a las lecturas desde el objeto estación
    lecturas = relationship("LecturaDB", back_populates="estacion")

class LecturaDB(Base):
    __tablename__ = "lecturas"
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float)
    estacion_id = Column(Integer, ForeignKey("estaciones.id"))
    
    estacion = relationship("EstacionDB", back_populates="lecturas")
>>>>>>> 22179523fa1522c3e634baeda63fd0eb3f454aa9
