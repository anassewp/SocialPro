"""Group management services."""
from __future__ import annotations

from typing import Iterable, List

from ..models import Group
from ..repositories import GroupRepository


class GroupService:
    """Service coordinating Telegram group membership."""

    def __init__(self, repository: GroupRepository) -> None:
        # تعليق: يحتفظ هذا الباني بمرجع المستودع لضمان الوصول إلى بيانات المجموعات.
        self._repository = repository

    def create_or_update_group(self, group_id: str, name: str | None = None) -> Group:
        """Create a group record or update its name."""

        # تعليق: تُنشئ هذه الدالة مجموعة جديدة أو تُحدّث الاسم المعروض للمجموعة الحالية.
        existing = self._repository.get(group_id)
        if existing:
            if name:
                existing.name = name
            group = existing
        else:
            group = Group(group_id=group_id, name=name or group_id)
        self._repository.save(group)
        return group

    def add_members(self, group_id: str, member_ids: Iterable[str]) -> Group:
        """Add multiple members to a group."""

        # تعليق: تضيف هذه الدالة مجموعة من الأعضاء إلى المجموعة وتضمن عدم التكرار.
        group = self._repository.get(group_id) or Group(group_id=group_id, name=group_id)
        for member in member_ids:
            if member not in group.members:
                group.members.append(member)
        self._repository.save(group)
        return group

    def list_groups(self) -> List[Group]:
        """Return all known groups."""

        # تعليق: تُرجع هذه الدالة جميع المجموعات المسجلة لإظهارها في لوحة التحكم.
        return self._repository.list_groups()
