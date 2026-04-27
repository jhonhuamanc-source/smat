from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_estacion():
    # Simulamos enviar un POST
    response = client.post(
        "/estaciones/", 
        json={"id": 99, "nombre": "Estacion de Prueba", "ubicacion": "Laboratorio FISI"}
    )
    # Validamos que responda con código 201 (Creado)
    assert response.status_code == 201
    assert response.json()["data"]["nombre"] == "Estacion de Prueba"
    
def test_registrar_lectura():
    # Simulamos registrar una lectura para la estación 99
    response = client.post(
        "/lecturas/", 
        json={"estacion_id": 99, "valor": 25.5}
    )
    assert response.status_code == 201

    
def test_obtener_historial():
    # Probamos el reto del historial
    response = client.get("/estaciones/99/historial")
    assert response.status_code == 200
    data = response.json()
    assert data["conteo"] >= 1
    assert data["promedio"] > 0
    

def test_riesgo_peligro():
    # 1. Registro de estación y lectura crítica (> 20.0)
    client.post("/estaciones/", json={"id": 10, "nombre": "Misti", "ubicacion": "Arequipa"})
    client.post("/lecturas/", json={"estacion_id": 10, "valor": 25.5})

    # 2. Prueba de endpoint de riesgo
    response = client.get("/estaciones/10/riesgo")
    assert response.status_code == 200
    assert response.json()["nivel"] == "PELIGRO"

def test_estacion_no_encontrada():
    # Probar un ID que no existe (ejemplo: 999)
    response = client.get("/estaciones/999/riesgo")
    assert response.status_code == 404
    assert response.json()["detail"] == "Estación no encontrada"    

def test_logica_niveles_riesgo():
    # Escenario 1: Probar nivel NORMAL (Valor <= 10.0)
    client.post("/lecturas/", json={"estacion_id": 99, "valor": 5.0})
    res_normal = client.get("/estaciones/99/riesgo")
    assert res_normal.json()["nivel"] == "NORMAL"

    # Escenario 2: Probar nivel ALERTA (10.0 < Valor <= 20.0)
    client.post("/lecturas/", json={"estacion_id": 99, "valor": 15.5})
    res_alerta = client.get("/estaciones/99/riesgo")
    assert res_alerta.json()["nivel"] == "ALERTA"

    # Escenario 3: Probar nivel PELIGRO (Valor > 20.0)
    client.post("/lecturas/", json={"estacion_id": 99, "valor": 25.0})
    res_peligro = client.get("/estaciones/99/riesgo")
    assert res_peligro.json()["nivel"] == "PELIGRO"

def test_estadisticas_globales():
    # Probamos el Dashboard del Laboratorio 4.3
    response = client.get("/estaciones/stats")
    assert response.status_code == 200
    data = response.json()
    # Verificamos que el JSON contenga las llaves esperadas
    assert "total_estaciones" in data
    assert "total_lecturas" in data
    assert "estacion_punto_critico" in data
