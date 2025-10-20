"""FastAPI application exposing SocialPro features."""
from __future__ import annotations

from typing import List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from socialpro.system import SocialProSystem

app = FastAPI(title="SocialPro", version="1.0.0")
system = SocialProSystem()


class AccountRequest(BaseModel):
    phone_number: Optional[str] = Field(None, description="Telegram phone number")
    user_id: Optional[str] = Field(None, description="Telegram user ID")
    alias: Optional[str] = Field(None, description="Display alias")


class MessageRequest(BaseModel):
    account_id: str = Field(..., description="Identifier of the sender account")
    recipients: List[str] = Field(..., description="List of recipients")
    message: str = Field(..., description="Message text")


class GroupMemberRequest(BaseModel):
    members: List[str] = Field(..., description="Members to add to the group")


class SubscriptionRequest(BaseModel):
    customer: str = Field(..., description="Customer identifier")
    plan_key: str = Field(..., description="Key of the subscription plan")


class DashboardResponse(BaseModel):
    messages: dict
    reports: list
    metrics: list


def get_language(accept_language: Optional[str] = Header(default="en")) -> str:
    """Resolve the preferred language from the request headers."""

    # تعليق: تحدد هذه الدالة اللغة المفضلة للطلب اعتمادًا على ترويسة Accept-Language.
    lang = (accept_language or "en").split(",")[0].strip()[:2]
    try:
        system.set_language(lang)
    except KeyError:
        system.set_language(system.config.default_language)
    return system.language


@app.post("/api/v1/accounts")
def create_account(payload: AccountRequest, language: str = Depends(get_language)):
    """Add a Telegram account using phone or user identifier."""

    # تعليق: تعالج هذه الدالة طلب إضافة حساب جديد وتعيد تفاصيل الحساب المضاف.
    try:
        account = system.add_telegram_account(phone_number=payload.phone_number, user_id=payload.user_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if payload.alias:
        account.alias = payload.alias
    return account


@app.get("/api/v1/accounts")
def list_accounts(language: str = Depends(get_language)):
    """List stored Telegram accounts."""

    # تعليق: تعرض هذه الدالة جميع الحسابات المسجلة لاستخدامها في واجهة الإدارة.
    return system.list_accounts()


@app.post("/api/v1/messages")
def send_message(payload: MessageRequest, language: str = Depends(get_language)):
    """Send individual or bulk Telegram messages."""

    # تعليق: تنفذ هذه الدالة إرسال الرسائل إلى المستلمين المحددين وتعيد سجلات الإرسال.
    try:
        logs = system.send_bulk_telegram_messages(
            account_id=payload.account_id,
            recipients=payload.recipients,
            message=payload.message,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return logs


@app.get("/api/v1/messages")
def list_messages(account_id: Optional[str] = None, language: str = Depends(get_language)):
    """Return stored message logs for auditing."""

    # تعليق: تعرض هذه الدالة سجلات الرسائل المرسلة مع إمكانية التصفية حسب الحساب للمراجعة.
    return system.list_messages(account_id=account_id)


@app.post("/api/v1/groups/{group_id}/members")
def add_group_members(group_id: str, payload: GroupMemberRequest, language: str = Depends(get_language)):
    """Add members to a Telegram group."""

    # تعليق: تضيف هذه الدالة مجموعة من الأعضاء إلى مجموعة محددة وتعيد حالة المجموعة الحالية.
    group = system.add_members_to_group(group_id=group_id, member_ids=payload.members)
    return group


@app.get("/api/v1/groups")
def list_groups(language: str = Depends(get_language)):
    """Return all managed groups."""

    # تعليق: تعرض هذه الدالة قائمة بالمجموعات والأعضاء المرتبطين بها للمتابعة الإدارية.
    return system.list_groups()


@app.get("/api/v1/subscriptions/plans")
def subscription_plans(language: str = Depends(get_language)):
    """List available subscription plans."""

    # تعليق: توفر هذه الدالة معلومات حول خطط الاشتراك الشهرية والسنوية للعرض على العملاء.
    return system.list_subscription_plans()


@app.post("/api/v1/subscriptions")
def activate_subscription(payload: SubscriptionRequest, language: str = Depends(get_language)):
    """Activate a subscription for a customer."""

    # تعليق: تُنشئ هذه الدالة اشتراكًا جديدًا أو تحدث اشتراكًا قائمًا للعميل المحدد.
    try:
        subscription = system.activate_subscription(customer=payload.customer, plan_key=payload.plan_key)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return subscription


@app.get("/api/v1/dashboard", response_model=DashboardResponse)
def dashboard(language: str = Depends(get_language)):
    """Return dashboard data including localized messages."""

    # تعليق: تجمع هذه الدالة بيانات لوحة التحكم لعرض الإحصائيات والرسائل المترجمة للمستخدم.
    snapshot = system.dashboard_snapshot()
    return DashboardResponse(**snapshot)
