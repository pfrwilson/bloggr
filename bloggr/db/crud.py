
from . import Session
from . import schemas, models

def get_user_from_id(db: Session, user_id: int) -> schemas.User | None:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return schemas.User.from_orm(user)
    

def get_user_from_name(db: Session, name: str) -> schemas.User | None:
    user = db.query(models.User).filter(models.User.name == name).first()
    return schemas.User.from_orm(user)


def create_user(db: Session, user_create: schemas.UserCreate): 
    user = models.User(**user_create.dict())
    try:
        db.add(user)
        db.commit()
    finally:
        db.close()
    

