from firebase_admin import messaging

def send_fcm_notification(title, body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            topic="sensor_alerts"
        )
        response = messaging.send(message)
        print(f"Notification sent: {response}")
        return response
    except Exception as e:
        print(f"Failed to send FCM notification: {e}")
        return None
