"""Domain models used by the SocialPro system."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Account:
    """Represents a Telegram account managed by the system."""

    identifier: str
    alias: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    platform: str = "telegram"


@dataclass
class MessageLog:
    """Represents a single message sending record."""

    account_id: str
    recipient: str
    message: str
    sent_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "sent"


@dataclass
class Group:
    """Represents a Telegram group with tracked members."""

    group_id: str
    name: Optional[str] = None
    members: List[str] = field(default_factory=list)


@dataclass
class SubscriptionPlan:
    """Represents a subscription plan available to customers."""

    name: str
    price_per_month: float
    billing_cycle: str  # "monthly" or "yearly"
    features: List[str]


@dataclass
class Subscription:
    """Represents an active subscription for an organization."""

    plan: SubscriptionPlan
    started_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


@dataclass
class InteractionMetric:
    """Aggregated metrics for analytics dashboards."""

    total_messages_sent: int = 0
    total_replies: int = 0
    conversion_rate: float = 0.0
    engagement_rate: float = 0.0
    extra: Dict[str, float] = field(default_factory=dict)


@dataclass
class Report:
    """Represents a marketing campaign report."""

    generated_at: datetime
    metrics: InteractionMetric
    notes: str = ""
