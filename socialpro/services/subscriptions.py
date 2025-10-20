"""Subscription management services."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from ..models import Subscription, SubscriptionPlan
from ..repositories import SubscriptionRepository, calculate_expiry


DEFAULT_PLANS: Dict[str, SubscriptionPlan] = {
    "monthly": SubscriptionPlan(
        name="Monthly",
        price_per_month=99.0,
        billing_cycle="monthly",
        features=[
            "telegram_basic_tools",
            "standard_reports",
        ],
    ),
    "yearly": SubscriptionPlan(
        name="Yearly",
        price_per_month=79.0,
        billing_cycle="yearly",
        features=[
            "telegram_basic_tools",
            "advanced_reports",
            "priority_support",
        ],
    ),
}


class SubscriptionService:
    """Service coordinating customer subscriptions."""

    def __init__(self, repository: SubscriptionRepository, plans: Dict[str, SubscriptionPlan] | None = None) -> None:
        # تعليق: يحفظ هذا الباني المستودع وقائمة الخطط المتاحة لإعادة استخدامها في العمليات.
        self._repository = repository
        self._plans = plans or DEFAULT_PLANS

    def list_plans(self) -> List[SubscriptionPlan]:
        """Return the available subscription plans."""

        # تعليق: تُرجع هذه الدالة جميع الخطط ليختار العميل ما يناسبه من حيث السعر والمزايا.
        return list(self._plans.values())

    def activate_subscription(self, customer: str, plan_key: str, start: datetime | None = None) -> Subscription:
        """Activate a plan for a customer and compute the expiry date."""

        # تعليق: تقوم هذه الدالة بتفعيل الاشتراك للعميل وتحديد تاريخ الانتهاء بناءً على نوع الخطة.
        if plan_key not in self._plans:
            raise KeyError(f"Plan {plan_key} is not available")
        start_date = start or datetime.utcnow()
        plan = self._plans[plan_key]
        expiry = calculate_expiry(start=start_date, billing_cycle=plan.billing_cycle)
        subscription = Subscription(plan=plan, started_at=start_date, expires_at=expiry)
        self._repository.upsert(customer, subscription)
        return subscription

    def get_subscription(self, customer: str) -> Subscription | None:
        """Return the subscription of a specific customer."""

        # تعليق: تسترجع هذه الدالة تفاصيل اشتراك العميل لمعرفة الحالة الحالية والمزايا المتاحة.
        return self._repository.get(customer)

    def clean_expired(self) -> None:
        """Remove expired subscriptions."""

        # تعليق: تحذف هذه الدالة الاشتراكات منتهية الصلاحية للحفاظ على بيانات حديثة وصحيحة.
        self._repository.purge_expired()
