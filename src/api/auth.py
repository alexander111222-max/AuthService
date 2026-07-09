import logging

from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from src.api.dependencies import PassManagerDep, DBDep, JWTManagerDep, UserIdDep
from src.config import settings
from src.schemas.users import UserRegisterSchema, LoginUserSchema
from src.services.refresh_tokens import RefreshTokensService
from src.services.users import UsersService
from src.utils.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    UserNotActiveException,
    WrongPasswordException,
    InvalidTokenError, RoleNotFoundException,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    description="Создаёт нового пользователя с ролью user. Пароль хранится в виде bcrypt хэша"
)
async def register_user(data: UserRegisterSchema, db: DBDep, password_manager: PassManagerDep):
    logger.info(f"Попытка регистрации пользователя с email: {data.email}")
    try:
        user = await UsersService(db).register(data, password_manager)
    except UserAlreadyExistsException:
        logger.warning(f"Регистрация отклонена - email уже занят: {data.email}")
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")
    except WrongPasswordException:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")
    except RoleNotFoundException:
        raise HTTPException(status_code=500, detail="Роль не найдена")
    logger.info(f"Пользователь успешно зарегистрирован: {data.email}")
    return user


@router.post(
    "/login",
    summary="Вход в систему",
    description="Проверяет email и пароль. При успехе устанавливает два httpOnly cookie: access_token (1 час) и refresh_token (30 дней)"
)
async def login_user(
    response: Response,
    data: LoginUserSchema,
    db: DBDep,
    password_manager: PassManagerDep,
    jwt_manager: JWTManagerDep,
):
    logger.info(f"Попытка входа пользователя с email: {data.email}")
    try:
        access_token = await UsersService(db).login(data.email, data.password, password_manager, jwt_manager)
        payload = jwt_manager.decode_token(access_token)
        refresh_token = await RefreshTokensService(db).create_refresh_token(
            user_id=payload["user_id"],
            jwt_manager=jwt_manager,
        )
    except UserNotFoundException:
        logger.warning(f"Вход отклонён - пользователь не найден: {data.email}")
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    except UserNotActiveException:
        logger.warning(f"Вход отклонён - аккаунт деактивирован: {data.email}")
        raise HTTPException(status_code=403, detail="Аккаунт деактивирован")
    except WrongPasswordException:
        logger.warning(f"Вход отклонён - неверный пароль: {data.email}")
        raise HTTPException(status_code=401, detail="Неверный пароль")

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=3600,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_TTL_DAYS * 24 * 3600,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    logger.info(f"Пользователь успешно вошёл: {data.email}")
    return {"status": "ok"}


@router.post(
    "/refresh",
    summary="Обновить access токен",
    description="Использует refresh_token из куки для выдачи нового access_token без повторного логина"
)
async def refresh_tokens(response: Response, request: Request, db: DBDep, jwt_manager: JWTManagerDep):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh токен отсутствует")

    logger.info("Попытка обновления access токена")
    try:
        access_token = await RefreshTokensService(db).refresh_access_token(refresh_token, jwt_manager)
    except (InvalidTokenError, UserNotFoundException):
        logger.warning("Обновление токена отклонено - невалидный refresh токен")
        raise HTTPException(status_code=401, detail="Невалидный или истёкший refresh токен")

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=3600,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    logger.info("Access токен успешно обновлён")
    return {"status": "ok"}


@router.post(
    "/logout",
    summary="Выход из системы",
    description="Удаляет refresh_token из БД и обе куки, завершая сессию пользователя",
)
async def logout_user(response: Response, db: DBDep, user_id: UserIdDep):
    logger.info(f"Выход пользователя с id: {user_id}")
    await RefreshTokensService(db).revoke_refresh_token(user_id)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"logout": "success"}