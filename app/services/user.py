from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, utils
from app.models import User
from app.repositories import UserRepository


async def create(user_create: schemas.UserCreate, db: Session):
    """Creates user"""

    user_repository = UserRepository(db)

    if await user_repository.get_user_by_email(user_create.email):
        raise HTTPException(status_code=400, detail="A user with that email exists.")

    user = User(**user_create.dict())
    user.password = utils.hash(user_create.password)

    return await user_repository.create(user)


async def get_user(user_id: int, db: Session):
    """Gets a user"""

    user_repository = UserRepository(db)
    user = await user_repository.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    return user


async def update(user: User, user_update: schemas.UserUpdateIn, db: Session):
    """Updates user info"""

    user_repository = UserRepository(db)

    if user_update.email and await user_repository.get_user_by_email(user_update.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email was found.",
        )

    return await user_repository.update(user, user_update)


async def change_password(
    user: User, user_update: schemas.UserChangePassword, db: Session
):
    """Changes user's password"""

    user_repository = UserRepository(db)
    user_update.password = utils.hash(user_update.password)

    return await user_repository.update(user, user_update)


async def delete(user: User, db: Session):
    """Deletes user"""

    user_repository = UserRepository(db)

    return await user_repository.delete(user)