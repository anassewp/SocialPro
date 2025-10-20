# SocialPro Documentation

## Overview
SocialPro is a modular marketing automation system focused on Telegram with a road map for extending the same workflow to other social networks. The platform combines account management, customer engagement tools, subscription billing, and reporting into a single Python-based codebase with a lightweight FastAPI front end.

## Features
- **Account Management:** Add and list Telegram accounts using phone numbers or user IDs.
- **Messaging Tools:** Send individual or bulk messages and retain message logs for analytics.
- **Group Member Management:** Maintain groups and append members in batches.
- **Analytics & Reporting:** Aggregate engagement metrics and generate dashboard-ready reports.
- **Subscription System:** Provide monthly and yearly plans with feature differentiation.
- **Localization:** Deliver prompts and dashboards in Arabic and English.

## Project Layout
```
SocialPro/
├── app.py                  # FastAPI application exposing HTTP endpoints
├── requirements.txt        # Python dependencies
├── socialpro/
│   ├── __init__.py         # Package exports
│   ├── config.py           # Application configuration objects
│   ├── localization.py     # Translation utilities
│   ├── models.py           # Data models for accounts, logs, plans, reports
│   ├── repositories.py     # In-memory repositories with helper utilities
│   ├── services/           # Business logic divided by concern
│   └── system.py           # High-level façade connecting services
└── docs/
    └── Documentation.md    # Detailed documentation (this file)
```

## Running the API Server
1. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Start the development server:**
   ```bash
   uvicorn app:app --reload
   ```
3. **Open the interactive docs:**
   Navigate to `http://127.0.0.1:8000/docs` to explore the automatically generated Swagger UI. All endpoints accept the `Accept-Language` header to toggle between Arabic (`ar`) and English (`en`).

## Core Modules
### `socialpro.system.SocialProSystem`
Acts as the main entry point coordinating repositories and services. It provides high-level methods for:
- Adding Telegram accounts.
- Sending individual and bulk messages.
- Managing groups and memberships.
- Activating subscriptions.
- Generating analytics reports and dashboard snapshots.

Because every method routes through this façade, integrating other platforms (e.g., Facebook, WhatsApp) only requires new repository/service implementations plus platform entries in `AppConfig.platforms`.

### Services
Each service focuses on a single business concern and uses Arabic comments to describe the intent of every method:
- `AccountService` – Validates and stores Telegram accounts.
- `MessagingService` – Records individual and bulk messaging activity.
- `GroupService` – Handles group creation and member aggregation.
- `AnalyticsService` – Converts message logs into reusable engagement metrics and reports.
- `SubscriptionService` – Manages subscription plans and expirations.
- `ReportingService` – Generates localized dashboard contexts.

### Repositories
The repositories provide in-memory storage for accounts, logs, groups, analytics metrics, reports, and subscriptions. They can be replaced with persistent storage backends without changing the service interfaces.

## Localization Strategy
Localized copy lives in `socialpro/localization.py`. The helper function `get_localized_message` centralizes translation lookup. Language preference propagates through the `ReportingService` and the FastAPI dependency `get_language`, ensuring a consistent experience across UI layers.

## Extending to New Platforms
To add support for another platform:
1. Create platform-specific repositories and services mirroring the Telegram implementations.
2. Register the platform in `AppConfig.platforms` with the relevant tool list.
3. Extend the FastAPI endpoints or front-end components to call the new service methods.
4. Update localization strings for the new platform prompts.

## External Integrations & Advanced Features
The current architecture accommodates future enhancements:
- **Real-Time Monitoring:** Replace the in-memory repositories with streaming analytics or message queues to capture live metrics.
- **Smart Messaging:** Introduce behavioral models in `MessagingService` to personalize content.
- **Machine Learning Analytics:** Augment `AnalyticsService` with ML-driven recommendations for send times and audience segmentation.
- **CRM Integrations:** Implement adapters inside `socialpro/services` to sync activity with Salesforce, HubSpot, or other CRMs.
- **External APIs:** Add modules that push analytics to Google Analytics, Zapier, or other automation tools.
- **Advanced Group Analytics:** Extend `GroupService` and `AnalyticsService` to record engagement rates per group.
- **UI Customization:** Layer a design system or theming engine on top of the FastAPI front end or migrate to a full-featured web client (React, Vue, etc.).

## Code Commenting Standard
All service and repository methods include descriptive Arabic comments alongside English docstrings, enabling bilingual developers to understand and maintain the system quickly.

## Testing Ideas
- Unit test services by injecting repositories with deterministic data.
- Write integration tests that spin up the FastAPI app using `TestClient` and assert endpoint behavior.
- Extend coverage to future platform connectors as they are introduced.

## Conclusion
SocialPro establishes a clear and extensible foundation for Telegram marketing automation. With modular services, bilingual support, and detailed documentation, the system is ready for both immediate deployment and future expansion to additional social networks.
