__all__ = ["router"]

import hashlib
import hmac

from fastapi import APIRouter, Request, Depends
from starlette.responses import HTMLResponse

from src.api.dependencies import UserIdDep, OptionalUserIdDep
from src.config import settings
from src.exceptions import InvalidTelegramWidgetHash, UnauthorizedException, AlreadyExists
from src.modules.providers.telegram.schemas import TelegramWidgetData, TelegramLoginResponse
from src.modules.user.repository import user_repository
from src.utils import aware_utcnow

router = APIRouter(prefix="/telegram")

if settings.telegram:

    def _get_secret_key() -> bytes:
        assert settings.telegram is not None
        bot_token: str = settings.telegram.bot_token.get_secret_value()
        secret_key = hashlib.sha256(bot_token.encode("utf-8"))  # noqa: HL
        return secret_key.digest()

    def validate_widget_hash(telegram_data: TelegramWidgetData) -> bool:
        """
        Verify telegram data

        https://core.telegram.org/widgets/login#checking-authorization
        """
        received_hash = telegram_data.hash
        encoded_telegarm_data = telegram_data.encoded
        evaluated_hash = hmac.new(_get_secret_key(), encoded_telegarm_data, hashlib.sha256).hexdigest()
        # check date
        _now = aware_utcnow().timestamp()
        if _now - 5 * 60 < telegram_data.auth_date < _now + 5 * 60:
            return evaluated_hash == received_hash
        return False

    @router.get(
        "/register",
        responses={
            200: {"description": "Success"},
            **InvalidTelegramWidgetHash.responses,
            **AlreadyExists.responses,
        },
        status_code=200,
    )
    async def telegram_register(
        user_id: OptionalUserIdDep, request: Request, telegram_data: TelegramWidgetData = Depends()
    ) -> None:
        if user_id is not None:
            raise AlreadyExists("Пользователь уже зарегистрирован (есть сессия)")
        if not validate_widget_hash(telegram_data):
            raise InvalidTelegramWidgetHash()
        user_by_telegram_id = await user_repository.read_by_telegram_id(telegram_data.id)
        if user_by_telegram_id is not None:
            raise AlreadyExists("Пользователь с таким telegram id уже существует")
        user = await user_repository.create_telegram(telegram_data)
        request.session.clear()
        request.session["uid"] = str(user.id)
        return None

    @router.get(
        "/connect",
        responses={
            200: {"description": "Success"},
            **InvalidTelegramWidgetHash.responses,
            **UnauthorizedException.responses,
        },
        status_code=200,
    )
    async def telegram_connect(user_id: UserIdDep, telegram_data: TelegramWidgetData = Depends()):
        if not validate_widget_hash(telegram_data):
            raise InvalidTelegramWidgetHash()
        await user_repository.update_telegram(user_id, telegram_data)

    @router.get(
        "/login",
        responses={
            200: {"description": "Success", "model": TelegramLoginResponse},
            **InvalidTelegramWidgetHash.responses,
            **UnauthorizedException.responses,
        },
    )
    async def telegram_login(
        user_id: OptionalUserIdDep, request: Request, telegram_data: TelegramWidgetData = Depends()
    ) -> TelegramLoginResponse:
        if not validate_widget_hash(telegram_data):
            raise InvalidTelegramWidgetHash()
        user_by_telegram_id = await user_repository.read_by_telegram_id(telegram_data.id)
        if user_by_telegram_id is None and user_id is not None:
            return TelegramLoginResponse(need_to_connect=True)
        if user_by_telegram_id is None:
            raise UnauthorizedException("Пользователь с таким telegram id не найден")
        request.session.clear()
        request.session["uid"] = str(user_by_telegram_id.id)
        return TelegramLoginResponse(need_to_connect=False)

    @router.get(
        "/register.html",
        responses={200: {"description": "Success"}},
        response_class=HTMLResponse,
    )
    async def telegram_register_html(request: Request) -> HTMLResponse:
        assert settings.telegram is not None
        register_url = request.url_for("telegram_register")

        script = f"""
        <script
            async src="https://telegram.org/js/telegram-widget.js?22"
            data-telegram-login="{settings.telegram.bot_username}"
            data-size="large"
            data-auth-url="{register_url}">
        </script>
        """

        html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Telegram Register Widget</title>
            </head>
            <body>
                <h1>Регистрация через Telegram</h1>
                {script}
            </body>
        </html>
        """

        return HTMLResponse(content=html)

    @router.get(
        "/connect.html",
        responses={200: {"description": "Success"}},
        response_class=HTMLResponse,
    )
    async def telegram_connect_html(request: Request) -> HTMLResponse:
        assert settings.telegram is not None

        connect_url = request.url_for("telegram_connect")

        script = f"""
        <script
            async src="https://telegram.org/js/telegram-widget.js?22"
            data-telegram-login="{settings.telegram.bot_username}"
            data-size="large"
            data-auth-url="{connect_url}">
        </script>
        """

        html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Telegram Login Widget</title>
            </head>
            <body>
                <h1>Подключение Telegram</h1>
                {script}
            </body>
        </html>
        """

        return HTMLResponse(content=html)

    @router.get(
        "/login.html",
        responses={200: {"description": "Success"}},
        response_class=HTMLResponse,
    )
    async def telegram_login_html(request: Request) -> HTMLResponse:
        assert settings.telegram is not None

        login_url = request.url_for("telegram_login")

        script = f"""
        <script
            async src="https://telegram.org/js/telegram-widget.js?22"
            data-telegram-login="{settings.telegram.bot_username}"
            data-size="large"
            data-auth-url="{login_url}">
        </script>
        """

        html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Telegram Login Widget</title>
            </head>
            <body>
                <h1>Вход через Telegram</h1>
                {script}
            </body>
        </html>
        """

        return HTMLResponse(content=html)
