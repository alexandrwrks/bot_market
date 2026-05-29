from fastapi import APIRouter, HTTPException, status

from market.crm.schemas.login import LoginUser
from market.crm.service import login_service
from market.crm.exceptions.login import EmailError, PasswordError

router = APIRouter()


@router.post("/login")
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
