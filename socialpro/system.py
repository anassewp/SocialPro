"""High-level façade for the SocialPro marketing platform."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from .config import AppConfig
from .models import Account, Group, MessageLog, Report, Subscription, SubscriptionPlan
from .repositories import (
    AccountRepository,
    AnalyticsRepository,
    GroupRepository,
    MessageLogRepository,
    ReportRepository,
    SubscriptionRepository,
)
from .services import (
    AccountService,
    AnalyticsService,
    GroupService,
    MessagingService,
    ReportingService,
    SubscriptionService,
)


@dataclass
class SocialProSystem:
    """Entry point that coordinates repositories and services."""

    config: AppConfig = field(default_factory=AppConfig)
    language: str = "en"
    _account_repo: AccountRepository = field(default_factory=AccountRepository, init=False)
    _message_repo: MessageLogRepository = field(default_factory=MessageLogRepository, init=False)
    _group_repo: GroupRepository = field(default_factory=GroupRepository, init=False)
    _analytics_repo: AnalyticsRepository = field(default_factory=AnalyticsRepository, init=False)
    _report_repo: ReportRepository = field(default_factory=ReportRepository, init=False)
    _subscription_repo: SubscriptionRepository = field(default_factory=SubscriptionRepository, init=False)

    def __post_init__(self) -> None:
        # تعليق: يقوم هذا الباني المتقدم بإنشاء الخدمات المختلفة وربطها مع المستودعات المطلوبة.
        self.accounts = AccountService(self._account_repo)
        self.messaging = MessagingService(self._message_repo)
        self.groups = GroupService(self._group_repo)
        self.subscriptions = SubscriptionService(self._subscription_repo)
        self.analytics = AnalyticsService(
            analytics_repo=self._analytics_repo,
            message_repo=self._message_repo,
            report_repo=self._report_repo,
        )
        self.reporting = ReportingService(language=self.language)

    def set_language(self, language: str) -> None:
        """Update the active language for the system."""

        # تعليق: تغيّر هذه الدالة لغة النظام وتضمن توحيدها مع خدمة التقارير.
        if language not in self.config.supported_languages:
            raise KeyError(f"Unsupported language: {language}")
        self.language = language
        self.reporting.set_language(language)

    def add_telegram_account(self, phone_number: Optional[str] = None, user_id: Optional[str] = None) -> Account:
        """Add a Telegram account using phone number or user identifier."""

        # تعليق: تسمح هذه الدالة بإضافة حساب تيليجرام سواءً برقم الهاتف أو معرف المستخدم وفقًا لمتطلبات اللوحة.
        identifier = phone_number or user_id
        if identifier is None:
            raise ValueError("Please enter either phone number or user ID.")
        return self.accounts.add_account(identifier=identifier, alias=identifier, platform="telegram")

    def send_telegram_message(self, account_id: str, recipient: str, message: str) -> MessageLog:
        """Send a single Telegram message."""

        # تعليق: ترسل هذه الدالة رسالة فردية عبر الحساب المحدد وتُخزن سجلًا بالعملية.
        return self.messaging.send_message(account_id=account_id, recipient=recipient, message=message)

    def send_bulk_telegram_messages(self, account_id: str, recipients: Iterable[str], message: str) -> List[MessageLog]:
        """Send a bulk Telegram message."""

        # تعليق: تُرسل هذه الدالة رسالة جماعية لمجموعة من المستلمين وتعيد جميع السجلات الناتجة.
        return self.messaging.send_bulk_messages(account_id=account_id, recipients=recipients, message=message)

    def add_members_to_group(self, group_id: str, member_ids: Iterable[str]) -> Group:
        """Add members to a Telegram group."""

        # تعليق: تضيف هذه الدالة مجموعة من المستخدمين إلى مجموعة تيليجرام مع الحفاظ على البيانات محدثة.
        self.groups.create_or_update_group(group_id)
        return self.groups.add_members(group_id=group_id, member_ids=member_ids)

    def activate_subscription(self, customer: str, plan_key: str) -> Subscription:
        """Activate a subscription for the customer."""

        # تعليق: تُفعّل هذه الدالة خطة اشتراك شهرية أو سنوية للعميل وتخزن التفاصيل.
        return self.subscriptions.activate_subscription(customer=customer, plan_key=plan_key)

    def list_subscription_plans(self) -> List[SubscriptionPlan]:
        """Return available subscription plans."""

        # تعليق: تعرض هذه الدالة الخطط الحالية ليختار العميل بين الاشتراك الشهري أو السنوي.
        return self.subscriptions.list_plans()

    def generate_telegram_report(self) -> Report:
        """Generate a fresh report for Telegram campaigns."""

        # تعليق: تُنشئ هذه الدالة تقرير أداء لحملات تيليجرام بالاعتماد على أحدث البيانات المتوفرة.
        self.analytics.record_daily_metrics(platform="telegram")
        return self.analytics.generate_report(platform="telegram")

    def dashboard_snapshot(self) -> Dict[str, object]:
        """Return the data required to render the dashboard."""

        # تعليق: تُحضّر هذه الدالة بيانات لوحة التحكم بما في ذلك الرسائل المترجمة والتقارير الحديثة.
        reports = self.analytics.list_reports()
        metrics = self._analytics_repo.list_metrics(platform="telegram")
        return self.reporting.dashboard_context(reports=reports, metrics=metrics)

    def list_accounts(self) -> List[Account]:
        """Return all managed accounts."""

        # تعليق: توفر هذه الدالة قائمة بالحسابات لعرضها في قسم إدارة الحسابات.
        return self.accounts.list_accounts()

    def list_groups(self) -> List[Group]:
        """Return all groups tracked by the system."""

        # تعليق: تعرض هذه الدالة جميع المجموعات بما فيها الأعضاء المضافين لتسهيل المتابعة.
        return self.groups.list_groups()

    def list_messages(self, account_id: Optional[str] = None) -> List[MessageLog]:
        """Return message logs, optionally filtered by account."""

        # تعليق: تسترجع هذه الدالة السجلات التاريخية للرسائل لإظهار نتائج الحملات التفصيلية.
        return self._message_repo.list_logs(account_id=account_id)

    def list_reports(self) -> List[Report]:
        """Return generated reports."""

        # تعليق: توفر هذه الدالة جميع التقارير المتاحة للاستعراض أو التحميل.
        return list(self.analytics.list_reports())

    def list_subscriptions(self) -> Dict[str, Subscription]:
        """Return the active subscriptions grouped by customer."""

        # تعليق: تعرض هذه الدالة الاشتراكات الحالية مع العملاء للاستعلام الإداري.
        return self._subscription_repo.list_subscriptions()
