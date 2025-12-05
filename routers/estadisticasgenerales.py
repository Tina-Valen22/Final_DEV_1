from fastapi import APIRouter
from models import Jugador, Estadisticageneral


router = APIRouter(prefix="/artistas", tags=["Artistas"])

@router.get("/", response_model=Jugador)
async def mostrar_estadisticas(Jugador_id:int):





