"""In-memory repositories for SocialPro entities."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Optional

from .models import Account, Group, InteractionMetric, MessageLog, Report, Subscription


class AccountRepository:
    """Repository responsible for storing account records."""

    def __init__(self) -> None:
        # تعليق: يقوم الباني بتهيئة قاموس لتخزين الحسابات بإستخدام المعرف كمفتاح.
        self._accounts: Dict[str, Account] = {}

    def add(self, account: Account) -> None:
        # تعليق: تضيف هذه الدالة حسابًا جديدًا إلى المستودع أو تستبدله إذا وُجد مسبقًا.
        self._accounts[account.identifier] = account

    def get(self, identifier: str) -> Optional[Account]:
        # تعليق: تُرجع هذه الدالة حسابًا محددًا بناءً على المعرف أو None إذا لم يوجد.
        return self._accounts.get(identifier)

    def list_accounts(self) -> List[Account]:
        # تعليق: تعيد هذه الدالة قائمة بجميع الحسابات المخزنة لإستخدامها في الواجهات.
        return list(self._accounts.values())


class MessageLogRepository:
    """Repository responsible for storing message logs."""

    def __init__(self) -> None:
        # تعليق: يهيئ هذا الباني قائمة لتجميع سجلات الرسائل المرسلة.
        self._logs: List[MessageLog] = []

    def add(self, log: MessageLog) -> None:
        # تعليق: تضيف هذه الدالة سجل رسالة جديد إلى القائمة لتتبع الأنشطة.
        self._logs.append(log)

    def list_logs(self, account_id: Optional[str] = None) -> List[MessageLog]:
        # تعليق: تُصفّي هذه الدالة السجلات حسب الحساب إذا طُلب ذلك أو تعيد جميع السجلات.
        if account_id is None:
            return list(self._logs)
        return [log for log in self._logs if log.account_id == account_id]


class GroupRepository:
    """Repository for storing group state."""

    def __init__(self) -> None:
        # تعليق: يهيئ هذا الباني قاموسًا لتخزين المجموعات حسب معرف المجموعة.
        self._groups: Dict[str, Group] = {}

    def save(self, group: Group) -> None:
        # تعليق: تحفظ هذه الدالة المجموعة وتمكن من تحديث بياناتها أو إضافتها لأول مرة.
        self._groups[group.group_id] = group

    def get(self, group_id: str) -> Optional[Group]:
        # تعليق: تُرجع هذه الدالة المجموعة المطلوبة أو None إذا لم تكن موجودة.
        return self._groups.get(group_id)

    def list_groups(self) -> List[Group]:
        # تعليق: تعيد هذه الدالة جميع المجموعات الموجودة لتسهيل عرضها للمستخدم.
        return list(self._groups.values())


class AnalyticsRepository:
    """Repository storing aggregate metrics by period."""

    def __init__(self) -> None:
        # تعليق: يستخدم هذا الباني قاموسًا متداخلًا لتجميع الإحصائيات اليومية.
        self._metrics: Dict[str, Dict[str, InteractionMetric]] = defaultdict(dict)

    def store_metric(self, date_key: str, platform: str, metric: InteractionMetric) -> None:
        # تعليق: تحفظ هذه الدالة بيانات التفاعل لمفتاح التاريخ والمنصة المحددين.
        self._metrics[platform][date_key] = metric

    def get_metric(self, date_key: str, platform: str) -> Optional[InteractionMetric]:
        # تعليق: تسترجع هذه الدالة بيانات التفاعل المخزنة أو None إن لم تتوفر.
        return self._metrics.get(platform, {}).get(date_key)

    def list_metrics(self, platform: str) -> Iterable[InteractionMetric]:
        # تعليق: تعيد هذه الدالة جميع الإحصائيات المرتبطة بالمنصة للمراجعة الشاملة.
        return self._metrics.get(platform, {}).values()


class ReportRepository:
    """Repository storing generated reports."""

    def __init__(self) -> None:
        # تعليق: يهيئ هذا الباني قائمة لحفظ التقارير المولدة للاستخدام المستقبلي.
        self._reports: List[Report] = []

    def add(self, report: Report) -> None:
        # تعليق: تضيف هذه الدالة تقريرًا جديدًا إلى القائمة مع الاحتفاظ بالترتيب الزمني.
        self._reports.append(report)

    def list_reports(self) -> List[Report]:
        # تعليق: تعيد هذه الدالة جميع التقارير المخزنة لإظهارها على لوحة التحكم.
        return list(self._reports)


class SubscriptionRepository:
    """Repository storing active subscriptions."""

    def __init__(self) -> None:
        # تعليق: يهيئ هذا الباني قاموسًا لمتابعة الاشتراكات حسب اسم العميل.
        self._subscriptions: Dict[str, Subscription] = {}

    def upsert(self, customer: str, subscription: Subscription) -> None:
        # تعليق: تُحدث هذه الدالة اشتراك العميل أو تضيفه إذا لم يكن موجودًا.
        self._subscriptions[customer] = subscription

    def get(self, customer: str) -> Optional[Subscription]:
        # تعليق: تُرجع هذه الدالة اشتراك العميل المحدد أو None عند عدم وجوده.
        return self._subscriptions.get(customer)

    def list_subscriptions(self) -> Dict[str, Subscription]:
        # تعليق: تعيد هذه الدالة جميع الاشتراكات الحالية على شكل قاموس للاطلاع السريع.
        return dict(self._subscriptions)

    def purge_expired(self, reference: Optional[datetime] = None) -> None:
        # تعليق: تزيل هذه الدالة الاشتراكات المنتهية تاريخيًا مقارنةً بالتاريخ المرجعي.
        now = reference or datetime.utcnow()
        expired = [key for key, sub in self._subscriptions.items() if sub.expires_at and sub.expires_at < now]
        for key in expired:
            del self._subscriptions[key]


def calculate_expiry(start: datetime, billing_cycle: str) -> datetime:
    """Calculate an expiry date based on the billing cycle."""

    # تعليق: تُحدد هذه الدالة تاريخ انتهاء الاشتراك اعتمادًا على الدورة الشهرية أو السنوية.
    if billing_cycle == "monthly":
        return start + timedelta(days=30)
    if billing_cycle == "yearly":
        return start + timedelta(days=365)
    raise ValueError(f"Unsupported billing cycle: {billing_cycle}")
