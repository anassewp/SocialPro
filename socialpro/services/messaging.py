"""Messaging utilities for Telegram interactions."""
from __future__ import annotations

from typing import Iterable, List

from ..models import MessageLog
from ..repositories import MessageLogRepository


class MessagingService:
    """Service responsible for sending Telegram messages."""

    def __init__(self, repository: MessageLogRepository) -> None:
        # تعليق: يحفظ هذا الباني مرجع مستودع السجلات لتوثيق جميع الرسائل المرسلة.
        self._repository = repository

    def send_message(self, account_id: str, recipient: str, message: str) -> MessageLog:
        """Send a single message and log the attempt."""

        # تعليق: تقوم هذه الدالة بمحاكاة إرسال رسالة فردية وتخزين سجلها في المستودع للمراجعة.
        if not all([account_id, recipient, message]):
            raise ValueError("Account, recipient, and message are required")
        log = MessageLog(account_id=account_id, recipient=recipient, message=message)
        self._repository.add(log)
        return log

    def send_bulk_messages(self, account_id: str, recipients: Iterable[str], message: str) -> List[MessageLog]:
        """Send the same message to many recipients and return the logs."""

        # تعليق: ترسل هذه الدالة رسالة موحدة إلى مجموعة من المستلمين وتعيد قائمة بالسجلات الناتجة.
        logs: List[MessageLog] = []
        for recipient in recipients:
            logs.append(self.send_message(account_id=account_id, recipient=recipient, message=message))
        return logs
