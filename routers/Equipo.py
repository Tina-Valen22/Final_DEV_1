from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Jugador, Estadisticageneral
from crud import create, get_all, update, delete, get_by_id
from filters import artistas_por_pais # << Nuevo: Importar función de filtro

router = APIRouter(prefix="/artistas", tags=["Artistas"])

@router.post("/")
def crear_jugador (jugador: Jugador, session: Session = Depends(get_session)):
    return create(session, Jugador, jugador)

@router.get("/")
def listar_artistas(session: Session = Depends(get_session)):
    return get_all(session, Artista)

@router.get("/{id}")
def obtener_artista(id: int, session: Session = Depends(get_session)):
    return get_by_id(session, Artista, id)

@router.put("/{id}")
def actualizar_artista(id: int, artista: Artista, session: Session = Depends(get_session)):
    return update(session, Artista, id, artista)

@router.delete("/{id}")
def eliminar_artista(id: int, session: Session = Depends(get_session)):
    return delete(session, Artista, id)

@router.get("/buscar/{nombre}")
def buscar_artista(nombre: str, session: Session = Depends(get_session)):
    return session.exec(
        select(Artista).where(Artista.nombre.ilike(f"%{nombre}%"), Artista.activo == True) # Ya estaba corregido
    ).all()

@router.get("/buscar/inactivo/{nombre}")
def buscar_artista_inactivo(nombre: str, session: Session = Depends(get_session)):
    """Busca artistas por nombre que estén INACTIVOS."""
    return session.exec(
        select(Artista).where(Artista.nombre.ilike(f"%{nombre}%"), Artista.activo == False)
    ).all()

@router.get("/filtrar/pais/{pais_id}")
def filtrar_artistas_por_pais(pais_id: int, session: Session = Depends(get_session)):
    return artistas_por_pais(pais_id, session=session)