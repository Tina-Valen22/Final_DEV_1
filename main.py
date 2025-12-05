from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import (
    Jugador, JugadorCreate,
    Estadistica, EstadisticaCreate,
    Partido, PartidoCreate
)

app = FastAPI(title="sigmotoa FC con SQLModel")


# Crear tablas al iniciar
@app.on_event("startup")
def startup():
    create_db_and_tables()


@app.get("/")
def home():
    return {"message": "sigmotoa FC API con SQLModel"}



@app.post("/jugadores/", response_model=Jugador)
def crear_jugador(jugador: JugadorCreate, session: Session = Depends(get_session)):
    nuevo = Jugador.from_orm(jugador)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


@app.get("/jugadores/")
def obtener_jugadores(session: Session = Depends(get_session)):
    jugadores = session.exec(select(Jugador)).all()
    return jugadores


@app.get("/jugadores/{jugador_id}")
def obtener_jugador(jugador_id: int, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(404, "Jugador no encontrado")
    return jugador


@app.delete("/jugadores/{jugador_id}")
def eliminar_jugador(jugador_id: int, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(404, "Jugador no encontrado")
    session.delete(jugador)
    session.commit()
    return {"message": "Jugador eliminado"}



@app.post("/estadisticas/")
def crear_estadistica(est: EstadisticaCreate, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, est.jugador_id)
    if not jugador:
        raise HTTPException(404, "Jugador no existe")

    nueva = Estadistica.from_orm(est)
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva


@app.get("/estadisticas/")
def obtener_estadisticas(session: Session = Depends(get_session)):
    return session.exec(select(Estadistica)).all()


@app.post("/partidos/")
def crear_partido(partido: PartidoCreate, session: Session = Depends(get_session)):
    nuevo = Partido.from_orm(partido)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


@app.get("/partidos/")
def obtener_partidos(session: Session = Depends(get_session)):
    return session.exec(select(Partido)).all()
