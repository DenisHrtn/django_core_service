import logging

from celery import shared_task
from django.conf import settings

from common_services.services.email_service import send_email_via_ses

logger = logging.getLogger(__name__)


@shared_task
def send_invite_token_to_email(to_address: str, token: str, project_name: str) -> None:
    """
    Таска для отправки письма с токеном для приглашения
    """
    try:
        domain = getattr(settings, "FRONTEND_DOMAIN", "http://127.0.0.1:8000")
        invite_url = f"{domain}/api/projects/accept-invite/"

        body = (
            f"Здравствуйте!\n\n"
            f"Вас пригласили принять участие в проекте **{project_name}**.\n\n"
            f"Ваш уникальный токен: **{token}**\n\n"
            f"Чтобы принять приглашение, перейдите по ссылке:\n{invite_url}\n\n"
            f"С уважением,\nКоманда проекта"
        )

        send_email_via_ses(
            subject="Вас пригласили участником в проект!",
            body=body,
            to_address=to_address,
        )

        logger.info(f"Письмо с приглашением успешно отправлено на {to_address}")
    except ValueError as exc:
        logger.error(f"Ошибка при отправке письма на {to_address}: {exc}")
