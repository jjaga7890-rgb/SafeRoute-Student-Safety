# SafeRoute — Enhanced Student Safety OS

A polished Django + REST + HTML/CSS/JavaScript school transport safety platform.

## What's enhanced
- Premium dark neo-noir violet / magenta UI
- Manrope + Space Grotesk + DM Mono typography
- Redesigned SafeRoute branding and navigation
- Command Center with operational KPIs and live workflow
- Fleet Management with richer vehicle cards and telemetry
- Student Management with searchable student cards and live journey panel
- RFID & Boarding Intelligence
- Cellular Intelligence with simulated cell visualization
- Routes & Stops
- ETA Intelligence
- Safety Center
- Notification Center
- Parent Portal
- Incident Command
- Trip Replay
- Analytics
- System Health
- Reports
- Responsive layout and mobile sidebar
- Existing Django API and automation cycle preserved

## Important positioning note
The cellular map is a simulation/approximation layer. It is not GPS and should not be presented as real-world triangulation accuracy without modem/network data.

## Run backend
Open PowerShell in:
`StudentSafetySystem\backend`

Run:
```powershell
python manage.py migrate
python manage.py runserver
```

Backend: http://127.0.0.1:8000/

## Run frontend
Open the `frontend` folder in VS Code and use Live Server on `index.html`.

Frontend: http://127.0.0.1:5500/StudentSafetySystem/frontend/index.html

Keep the backend terminal running while using the frontend.
