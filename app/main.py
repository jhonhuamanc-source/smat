from fastapi import FastAPI, Depends, HTTPException
from fastapi import FastAPI
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app import models, schemas, crud
from app.database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)

from app.database import engine, get_db
app = FastAPI(title="SMAT Backend Profesional")

# Configuración de orígenes permitidos
origins = ["*"] # En producción, especificar dominios reales
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EstacionCreate(BaseModel):
    id: int
    nombre: str
    ubicacion: str



@app.post(
    "/estaciones/",
    status_code=201,
    tags=["Gestión de Infraestructura"],
    summary="Registrar una nueva estación de monitoreo",
    description="Inserta una estación física (ej. río, volcán, zona sísmica) en la base de datos relacional."
)
def crear_estacion(estacion: EstacionCreate, db: Session = Depends(get_db)):
    nueva_estacion = models.EstacionDB(id=estacion.id, nombre=estacion.nombre, ubicacion=estacion.ubicacion)
    db.add(nueva_estacion)
    db.commit()
    db.refresh(nueva_estacion)
    return {"msj": "Estación guardada en DB", "data": nueva_estacion} #

@app.get("/estaciones/")
def listar_estaciones(db: Session = Depends(get_db)):
    # Esta línea hace la consulta SQL: SELECT * FROM estaciones;
    estaciones = db.query(models.EstacionDB).all()
    return estaciones

class LecturaCreate(BaseModel):
    estacion_id: int
    valor: float



@app.post(
    "/lecturas/",
    status_code=201,
    tags=["Telemetría de Sensores"],
    summary="Recibir datos de telemetría",
    description="Recibe el valor capturado por un sensor y lo vincula a una estación existente mediante su ID."
)
def registrar_lectura(lectura: LecturaCreate, db: Session = Depends(get_db)):
    # Validar si la estación existe en la DB
    estacion = db.query(models.EstacionDB).filter(models.EstacionDB.id ==
lectura.estacion_id).first()
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no existe")

    nueva_lectura = models.LecturaDB(valor=lectura.valor,
estacion_id=lectura.estacion_id)
    db.add(nueva_lectura)
    db.commit()
    return {"status": "Lectura guardada en DB"}

@app.get("/lecturas/")
def listar_lecturas(db: Session = Depends(get_db)):
    # Esta línea hace la consulta SQL: SELECT * FROM estaciones;
    lecturas = db.query(models.LecturaDB).all()
    return lecturas


@app.get(
    "/estaciones/stats", 
    tags=["Auditoría"],
    summary="Resumen ejecutivo del sistema",
    description="""
    Retorna un reporte global que incluye:
    - Total de estaciones monitoreadas en la red.
    - Cantidad total de lecturas procesadas históricamente.
    - Identificación de la estación con el valor de lectura más alto (punto crítico).
    """
)
def obtener_estadisticas_globales(db: Session = Depends(get_db)):
    return crud.obtener_estadisticas_globales(db)


@app.get(
    "/estaciones/{id}/riesgo",
    tags=["Análisis de Riesgo"],
    summary="Evaluar nivel de peligro actual",
    description="Analiza la última lectura recibida de una estación y determina si el estado es NORMAL, ALERTA o PELIGRO."
)
def obtener_riesgo(id: int, db: Session = Depends(get_db)):
    # 1. Validar existencia en DB 
    estacion = db.query(models.EstacionDB).filter(models.EstacionDB.id == id).first()
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")

    # 2. Obtener lecturas de la DB 
    lecturas = db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == id).all()
    
    if not lecturas:
        return {"id": id, "nivel": "SIN DATOS", "valor": 0}

    # 3. Evaluar última lectura (la última de la lista)
    ultima_lectura = lecturas[-1].valor
    
    if ultima_lectura > 20.0:
        nivel = "PELIGRO" 
    elif ultima_lectura > 10.0:
        nivel = "ALERTA" 
    else:
        nivel = "NORMAL" 

    return {"id": id, "valor": ultima_lectura, "nivel": nivel} 


@app.get("/estaciones/{id}/historial")
def obtener_historial(id: int, db: Session = Depends(get_db)):
    # 1. Verificar si la estación existe en la DB 
    estacion = db.query(models.EstacionDB).filter(models.EstacionDB.id == id).first()
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")

    # 2. Filtrar lecturas desde la DB 
    lecturas_db = db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == id).all()
    
    # 3. Extraer solo los valores para el cálculo 
    valores = [l.valor for l in lecturas_db]
    
    # 4. Cálculo del promedio 
    promedio = sum(valores) / len(valores) if valores else 0.0

    return {
        "estacion_id": id,
        "lecturas": valores,
        "conteo": len(valores),
        "promedio": round(promedio, 2)
    }