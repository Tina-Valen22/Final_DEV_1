from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class JugadorBase(SQLModel):
    nombre: str
    edad: int
    posicion: Position
    estado: States


class Jugador(JugadorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    estadisticas: List["Estadistica"] = Relationship(back_populates="jugador")


class JugadorCreate(JugadorBase):
    pass



class EstadisticaBase(SQLModel, table=True):
    goles: int = 0
    asistencias: int = 0
    partidos_jugados: int = 0

class EstadisticaPartidos(SQLModel):
    goles: int
    asistencias: int
    minutos_jugados: int
    faltas_cometidas: int
    tarjeta_amarilla: bool
    tarjeta_roja: bool
    lesion: bool


class Estadistica(EstadisticaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jugador_id: Optional[int] = Field(default=None, foreign_key="jugador.id")

    jugador: Optional[Jugador] = Relationship(back_populates="estadisticas")


class EstadisticaCreate(EstadisticaBase):
    jugador_id: int


class PartidoBase(SQLModel):
    equipo_local: str
    equipo_visitante: str
    marcador_local: int = 0
    marcador_visitante: int = 0
    fecha: str


class Partido(PartidoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class PartidoCreate(PartidoBase):
    pass
