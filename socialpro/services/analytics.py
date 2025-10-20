"""Analytics and reporting helpers."""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional

from ..models import InteractionMetric, MessageLog, Report
from ..repositories import AnalyticsRepository, MessageLogRepository, ReportRepository


class AnalyticsService:
    """Service providing aggregated marketing analytics."""

    def __init__(
        self,
        analytics_repo: AnalyticsRepository,
        message_repo: MessageLogRepository,
        report_repo: ReportRepository,
    ) -> None:
        # تعليق: يحفظ هذا الباني مراجع المستودعات اللازمة لحساب المؤشرات وإنشاء التقارير.
        self._analytics_repo = analytics_repo
        self._message_repo = message_repo
        self._report_repo = report_repo

    def record_daily_metrics(self, platform: str, logs: Optional[Iterable[MessageLog]] = None) -> InteractionMetric:
        """Aggregate metrics for a platform using the provided logs."""

        # تعليق: تحسب هذه الدالة إجمالي الرسائل والتفاعل اليومي وتخزن النتائج في مستودع التحليلات.
        if logs is None:
            logs = self._message_repo.list_logs()
        total_messages = 0
        total_replies = 0
        for log in logs:
            total_messages += 1
            if "reply" in log.status:
                total_replies += 1
        engagement_rate = (total_replies / total_messages) * 100 if total_messages else 0.0
        metric = InteractionMetric(
            total_messages_sent=total_messages,
            total_replies=total_replies,
            engagement_rate=engagement_rate,
        )
        date_key = datetime.utcnow().strftime("%Y-%m-%d")
        self._analytics_repo.store_metric(date_key=date_key, platform=platform, metric=metric)
        return metric

    def generate_report(self, platform: str) -> Report:
        """Generate and store a report for a platform."""

        # تعليق: تُنشئ هذه الدالة تقريرًا جديدًا باستخدام أحدث المؤشرات وتخزنه للاطلاع لاحقًا.
        metrics = list(self._analytics_repo.list_metrics(platform))
        summary_metric = metrics[-1] if metrics else InteractionMetric()
        report = Report(generated_at=datetime.utcnow(), metrics=summary_metric)
        self._report_repo.add(report)
        return report

    def list_reports(self) -> Iterable[Report]:
        """Return all stored reports."""

        # تعليق: تُرجع هذه الدالة جميع التقارير المولدة لعرضها في قسم التحليلات.
        return self._report_repo.list_reports()
