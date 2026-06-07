from fastapi import APIRouter, HTTPException, status

from app.api.exceptions.login import EmailError, PasswordError
from app.api.schemas.login import LoginUser
from app.api.service import login_service

router = APIRouter()


@router.post("/login/")
async def register(user: LoginUser):
    try:
        await login_service.login_user(user)

    except EmailError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email",
        )

    except PasswordError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
