"""Localization utilities for bilingual messaging."""
from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "add_account_prompt": "Enter the phone number or user ID of the Telegram account to add it.",
        "dashboard_overview": "Here you can monitor your campaigns on Telegram, update messages, and analyze customer data.",
        "subscription_prompt": "Select a subscription plan that fits your needs with additional benefits for yearly subscribers.",
        "telegram_tools_prompt": "Use these tools to reach your customers via Telegram with personalized messages.",
        "analytics_prompt": "View live reports to analyze the performance of your campaigns on Telegram.",
    },
    "ar": {
        "add_account_prompt": "أدخل رقم الهاتف أو معرف المستخدم لحساب تيليجرام لإضافته.",
        "dashboard_overview": "هنا يمكنك متابعة حملاتك على تيليجرام وتحديث الرسائل وتحليل بيانات العملاء.",
        "subscription_prompt": "اختر خطة الاشتراك التي تناسب احتياجاتك مع مزايا إضافية للمشتركين السنويين.",
        "telegram_tools_prompt": "استخدم هذه الأدوات للوصول إلى عملائك عبر تيليجرام برسائل مخصصة.",
        "analytics_prompt": "اعرض التقارير الحية لتحليل أداء حملاتك على تيليجرام.",
    },
}


def get_localized_message(language: str, key: str) -> str:
    """Return a localized message for the requested key."""

    # تعليق: تُعيد هذه الدالة النص المترجم بناءً على اللغة والمفتاح المطلوب.
    return TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(key, "")
