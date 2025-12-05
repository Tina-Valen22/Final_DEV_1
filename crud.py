from fastapi import HTTPException
from sqlmodel import Session, select
from typing import Type, TypeVar

T = TypeVar("T")


def create(session: Session, model: Type[T], data: T):
    try:
        session.add(data)
        session.commit()
        session.refresh(data)
        return data
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear: {e}")


def get_all(session: Session, model: Type[T]):
    if hasattr(model, 'activo'):
        return session.exec(select(model).where(model.activo == True)).all()
    else:
        return session.exec(select(model)).all()



def get_by_id(session: Session, model: Type[T], id: int):
    instance = session.get(model, id)
    if not instance:
        raise HTTPException(status_code=404, detail=f"{model.__name__} no encontrado.")

    # Comprobar 'activo' solo si el modelo tiene el atributo
    if hasattr(instance, 'activo') and not instance.activo:
        raise HTTPException(status_code=404, detail=f"{model.__name__} no encontrado o inactivo.")

    return instance


def update(session: Session, model: Type[T], id: int, data: T):
    instance = session.get(model, id)
    if not instance:
        raise HTTPException(status_code=404, detail=f"{model.__name__} no encontrado.")

    if hasattr(instance, 'activo') and not instance.activo:
        raise HTTPException(status_code=404, detail=f"{model.__name__} no encontrado o inactivo.")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(instance, key, value)

    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance


def delete(session: Session, model: Type[T], id: int):
    instance = session.get(model, id)
    if not instance:
        raise HTTPException(status_code=404, detail=f"{model.__name__} no encontrado.")

    if hasattr(instance, 'activo'):
        instance.activo = False
        session.add(instance)
        session.commit()
        return {"mensaje": f"{model.__name__} eliminado (lógicamente) correctamente."}
    else:

        session.delete(instance)
        session.commit()
        return {"mensaje": f"{model.__name__} eliminado (físicamente) correctamente."}