"""Reporting utilities for dashboards."""
from __future__ import annotations

from typing import Dict, Iterable

from ..localization import get_localized_message
from ..models import InteractionMetric, Report


class ReportingService:
    """Service producing dashboard-friendly data structures."""

    def __init__(self, language: str = "en") -> None:
        # تعليق: يحدد هذا الباني اللغة الافتراضية للرسائل المعروضة في لوحة التحكم.
        self._language = language

    def set_language(self, language: str) -> None:
        """Update the active language for the reporting interface."""

        # تعليق: تقوم هذه الدالة بتغيير اللغة المستخدمة لعرض الرسائل لضمان دعم العربية والإنجليزية.
        self._language = language

    def dashboard_context(self, reports: Iterable[Report], metrics: Iterable[InteractionMetric]) -> Dict[str, object]:
        """Build a dictionary used by the dashboard interface."""

        # تعليق: تنشئ هذه الدالة سياقًا شاملاً للوحة التحكم يجمع التقارير والرسائل المترجمة.
        return {
            "messages": {
                key: get_localized_message(self._language, key)
                for key in [
                    "add_account_prompt",
                    "dashboard_overview",
                    "subscription_prompt",
                    "telegram_tools_prompt",
                    "analytics_prompt",
                ]
            },
            "reports": list(reports),
            "metrics": list(metrics),
        }
