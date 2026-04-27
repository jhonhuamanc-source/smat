<<<<<<< HEAD
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Definimos el nombre del archivo. Si no existe, SQLite lo creará automáticamente.

SQLALCHEMY_DATABASE_URL = "sqlite:///./smat.db"
# 2. Creamos el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL,
connect_args={"check_same_thread": False})

# 3. Creamos una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Clase base para los modelos
Base = declarative_base()

# 5. Dependencia para inyectar la DB en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
=======
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Definimos el nombre del archivo. Si no existe, SQLite lo creará automáticamente.

SQLALCHEMY_DATABASE_URL = "sqlite:///./smat.db"
# 2. Creamos el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL,
connect_args={"check_same_thread": False})

# 3. Creamos una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Clase base para los modelos
Base = declarative_base()

# 5. Dependencia para inyectar la DB en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
>>>>>>> 22179523fa1522c3e634baeda63fd0eb3f454aa9
