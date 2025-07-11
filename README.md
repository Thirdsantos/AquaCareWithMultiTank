#  AquaCareWithMultiTanks

A comprehensive Flask-based REST API for intelligent monitoring of multiple aquarium tanks with AI-powered fish identification and water parameter analysis.

## Features

- **Multi-Tank Management**: Monitor multiple aquariums independently
- **Real-Time Sensor Monitoring**: Track pH, temperature, and turbidity
- **AI-Powered Fish Identification**: Identify fish species and get water parameters via Google Gemini
- **Smart Notification System**: Individual notification channels for each sensor type
- **Data Analytics**: Hourly logging and daily average calculations
- **Firebase Integration**: Secure data persistence and real-time updates
- **CORS Enabled**: Ready for frontend integration

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: Firebase Realtime Database
- **AI**: Google Gemini 1.5 Flash
- **Notifications**: Firebase Cloud Messaging
- **Deployment**: Render

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see DEPLOYMENT.md)
4. Run: `python run.py`

##  API Endpoints

- `POST /ask` - AI chat and fish analysis
- `POST /aquarium/{id}/sensor` - Sensor data input
- `POST /aquarium/{id}/log_per_hour` - Hourly data logging




