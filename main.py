from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configuración de tu base de datos MySQL (XAMPP por defecto)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="soporte_app"
    )


class Incidencia(BaseModel):
    nombre_usuario: str
    correo: str
    numero_equipo: int
    descripcion: str
    prioridad: str
    estado: str

# 1. GET: Obtener todas las incidencias


@app.get("/api/incidencias")
def get_incidencias():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM incidencias")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# 2. GET por ID: Obtener una incidencia específica


@app.get("/api/incidencias/{id}")
def get_incidencia(id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM incidencias WHERE id = %s", (id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    return result

# 3. POST: Crear una incidencia


@app.post("/api/incidencias", status_code=201)
def create_incidencia(incidencia: Incidencia):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO incidencias 
             (nombre_usuario, correo, numero_equipo, descripcion, prioridad, estado, fecha_registro) 
             VALUES (%s, %s, %s, %s, %s, %s, NOW())"""
    val = (incidencia.nombre_usuario, incidencia.correo, incidencia.numero_equipo,
           incidencia.descripcion, incidencia.prioridad, incidencia.estado)
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Incidencia registrada correctamente"}

# 4. PUT: Editar una incidencia


@app.put("/api/incidencias/{id}")
def update_incidencia(id: int, incidencia: Incidencia):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """UPDATE incidencias SET 
             nombre_usuario=%s, correo=%s, numero_equipo=%s, descripcion=%s, prioridad=%s, estado=%s 
             WHERE id=%s"""
    val = (incidencia.nombre_usuario, incidencia.correo, incidencia.numero_equipo,
           incidencia.descripcion, incidencia.prioridad, incidencia.estado, id)
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Incidencia actualizada correctamente"}

# 5. DELETE: Eliminar una incidencia


@app.delete("/api/incidencias/{id}")
def delete_incidencia(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM incidencias WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Incidencia eliminada"}
