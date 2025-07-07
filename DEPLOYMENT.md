# Deployment Guide for Render

## Environment Variables Setup

### Required Environment Variables:

1. **GEMINI_API_KEY**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Add it to your Render environment variables

2. **FIREBASE_CREDENTIALS** (for production)
   - Get your Firebase service account key from Firebase Console
   - Convert the JSON file to a single line string
   - Add it to your Render environment variables

3. **FIREBASE_DATABASE_URL** (optional)
   - Your Firebase Realtime Database URL
   - Default: `https://ac-with-multitank-default-rtdb.asia-southeast1.firebasedatabase.app/`

### How to Set Environment Variables in Render:

1. Go to your Render dashboard
2. Select your service
3. Go to "Environment" tab
4. Add the following environment variables:

   ```
   Key: GEMINI_API_KEY
   Value: your_actual_gemini_api_key_here
   ```

   ```
   Key: FIREBASE_CREDENTIALS
   Value: {"type":"service_account","project_id":"your-project","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"..."}
   ```

   ```
   Key: FIREBASE_DATABASE_URL
   Value: https://your-project-default-rtdb.asia-southeast1.firebasedatabase.app/
   ```

### How to Convert Firebase JSON to Environment Variable:

1. Open your `app/utils/key.json` file
2. Copy the entire JSON content
3. Remove all line breaks and spaces (make it one line)
4. Paste it as the value for `FIREBASE_CREDENTIALS`

## Local Development Setup

1. Create a `.env` file in your project root:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   FIREBASE_DATABASE_URL=https://ac-with-multitank-default-rtdb.asia-southeast1.firebasedatabase.app/
   ```

2. Keep your `app/utils/key.json` file for local development

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python run.py
   ```

## API Endpoints

### AI Chat Endpoint:
```
POST /ask
Content-Type: application/json

{
  "question": "What's the best pH for goldfish?",
  "image": "base64_image_data",  // optional
  "aquarium_id": "aquarium_001"  // optional
}
```

### Sensor Data Endpoint:
```
POST /aquarium/{aquarium_id}/sensor
Content-Type: application/json

{
  "ph": 7.2,
  "temperature": 25.5,
  "turbidity": 15.0
}
```

### Hourly Log Endpoint:
```
POST /aquarium/{aquarium_id}/log_per_hour
Content-Type: application/json

{
  "ph": 7.2,
  "temperature": 25.5,
  "turbidity": 15.0
}
```

## CORS Enabled

The application now supports cross-origin requests, making it suitable for frontend integration.

## Firebase Configuration

The application now supports both:
- **Local Development**: Uses `app/utils/key.json` file
- **Production**: Uses `FIREBASE_CREDENTIALS` environment variable

This makes it secure for deployment while keeping local development simple. 