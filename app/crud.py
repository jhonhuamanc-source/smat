# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas

# ==========================================
# 1. GESTIÓN DE INFRAESTRUCTURA (Estaciones)
# ==========================================

def crear_estacion(db: Session, estacion: schemas.EstacionCreate):
    nueva_estacion = models.EstacionDB(**estacion.dict())
    db.add(nueva_estacion)
    db.commit()
    db.refresh(nueva_estacion)
    return nueva_estacion

def obtener_estacion(db: Session, estacion_id: int):
    # Busca si existe una estación específica
    return db.query(models.EstacionDB).filter(models.EstacionDB.id == estacion_id).first()

def listar_estaciones(db: Session):
    return db.query(models.EstacionDB).all()


# ==========================================
# 2. TELEMETRÍA DE SENSORES (Lecturas)
# ==========================================

def registrar_lectura(db: Session, lectura: schemas.LecturaCreate):
    nueva_lectura = models.LecturaDB(**lectura.dict())
    db.add(nueva_lectura)
    db.commit()
    return nueva_lectura

def obtener_lecturas_por_estacion(db: Session, estacion_id: int):
    # Devuelve todas las lecturas asociadas a un ID de estación
    return db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == estacion_id).all()


# ==========================================
# 3. LÓGICA DE NEGOCIO (Riesgo e Historial)
# ==========================================

def calcular_riesgo(db: Session, estacion_id: int):
    lecturas = obtener_lecturas_por_estacion(db, estacion_id)
    
    if not lecturas:
        return {"id": estacion_id, "nivel": "SIN DATOS", "valor": 0}
    
    ultima_lectura = lecturas[-1].valor
    nivel = "PELIGRO" if ultima_lectura > 20.0 else "ALERTA" if ultima_lectura > 10.0 else "NORMAL"
    
    return {"id": estacion_id, "valor": ultima_lectura, "nivel": nivel}

def calcular_historial(db: Session, estacion_id: int):
    lecturas = obtener_lecturas_por_estacion(db, estacion_id)
    valores = [l.valor for l in lecturas]
    
    promedio = sum(valores) / len(valores) if valores else 0.0
    
    return {
        "estacion_id": estacion_id,
        "lecturas": valores,
        "conteo": len(valores),
        "promedio": round(promedio, 2)
    }
    
    # app/crud.py

def obtener_estadisticas_globales(db: Session):
    # 1. Conteo de estaciones
    total_estaciones = db.query(models.EstacionDB).count()
    
    # 2. Conteo de lecturas
    total_lecturas = db.query(models.LecturaDB).count()
    
    # 3. Estación con el valor más alto (Punto crítico)
    lectura_maxima = db.query(models.LecturaDB).order_by(models.LecturaDB.valor.desc()).first()
    
    punto_critico_id = lectura_maxima.estacion_id if lectura_maxima else None
    valor_maximo = lectura_maxima.valor if lectura_maxima else 0.0
        
    return {
        "total_estaciones": total_estaciones,
        "total_lecturas": total_lecturas,
        "estacion_punto_critico": punto_critico_id,
        "valor_maximo": valor_maximo
    }