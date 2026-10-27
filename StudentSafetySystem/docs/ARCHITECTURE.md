# Architecture
Frontend -> REST API -> Django services/models -> SQLite/PostgreSQL.
Device adapters -> API -> identity/location/safety/ETA processing -> dashboard and notifications.
The simulator uses the same API pathway so the UI can be tested before hardware is installed.
