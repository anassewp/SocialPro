"""Account management services."""
from __future__ import annotations

from typing import List, Optional

from ..models import Account
from ..repositories import AccountRepository


class AccountService:
    """Service responsible for managing messaging accounts."""

    def __init__(self, repository: AccountRepository) -> None:
        # تعليق: يُخزن هذا الباني مرجعًا لمستودع الحسابات لإعادة استخدامه في جميع العمليات.
        self._repository = repository

    def add_account(self, identifier: str, alias: Optional[str] = None, platform: str = "telegram") -> Account:
        """Create and store an account record."""

        # تعليق: تنشئ هذه الدالة حسابًا جديدًا وتضيفه إلى المستودع بعد التحقق الأساسي من المعرف.
        if not identifier:
            raise ValueError("Account identifier is required")
        account = Account(identifier=identifier, alias=alias, platform=platform)
        self._repository.add(account)
        return account

    def get_account(self, identifier: str) -> Optional[Account]:
        """Retrieve a specific account by identifier."""

        # تعليق: تستدعي هذه الدالة المستودع لاسترجاع الحساب المطلوب حسب المعرف المقدم.
        return self._repository.get(identifier)

    def list_accounts(self) -> List[Account]:
        """Return all stored accounts."""

        # تعليق: تُرجع هذه الدالة قائمة بجميع الحسابات لعرضها في لوحة التحكم أو الواجهات الأخرى.
        return self._repository.list_accounts()
