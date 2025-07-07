from app.utils.firebase import firebase_db
from app.services.notification_service import send_fcm_notification
from datetime import datetime, timezone

def get_sensors(aquarium_id):
  ref = firebase_db.reference(f"{aquarium_id}/sensors")
  return ref.get()

def save_sensors(aquarium_id, sensors):
  ref_latest_id = firebase_db.reference(f"{aquarium_id}/logs_per_hour/latest_id")
  latest_id = ref_latest_id.get()
  if latest_id is None:
    ref_latest_id.set(0)
  ref = firebase_db.reference(f"{aquarium_id}/sensors")
  ref.set(sensors)

def save_log_per_hour(aquarium_id, sensors):
    # Get latest log ID
    ref_latest_id = firebase_db.reference(f"{aquarium_id}/logs_per_hour/latest_id")
    latest_id = ref_latest_id.get() or 0
    new_id = latest_id + 1

    # Save new hourly log
    firebase_db.reference(f"{aquarium_id}/logs_per_hour/{new_id}").set(sensors)
    ref_latest_id.set(new_id)

    # Check if we've reached 24 hours (daily cycle)
    if new_id % 24 == 0:
        average = {
            "ph": 0,
            "temperature": 0,
            "turbidity": 0
        }
        logs = firebase_db.reference(f"{aquarium_id}/logs_per_hour").get()
        if not logs:
            return

        ph_values, temp_values, turb_values = [], [], []

        # Collect values from the last 24 logs (1-24)
        for i in range(1, 25):  # 1 to 24 inclusive
            log_key = str(i)
            if log_key in logs and logs[log_key]:
                log_data = logs[log_key]
                if "ph" in log_data and "temperature" in log_data and "turbidity" in log_data:
                    ph_values.append(log_data["ph"])
                    temp_values.append(log_data["temperature"])
                    turb_values.append(log_data["turbidity"])

        # Calculate averages only if we have valid data
        if len(ph_values) > 0:
            average["ph"] = round(sum(ph_values) / len(ph_values), 2)
            average["temperature"] = round(sum(temp_values) / len(temp_values), 2)
            average["turbidity"] = round(sum(turb_values) / len(turb_values), 2)

            # Save daily average
            average_per_day(aquarium_id, average)

        # Clear only the hourly logs (1-24), keep latest_id
        for i in range(1, 25):
            firebase_db.reference(f"{aquarium_id}/logs_per_hour/{i}").delete()

        # Reset latest_id to 0 for the next day
        ref_latest_id.set(0)

def average_per_day(aquarium_id, average):
    # Validate average data before saving
    if not average or not all(key in average for key in ["ph", "temperature", "turbidity"]):
        print(f"Invalid average data for aquarium {aquarium_id}")
        return
    
    ref_latest_id = firebase_db.reference(f"{aquarium_id}/average/latest_id")
    latest_id = ref_latest_id.get() or 0
    new_id = latest_id + 1

    # Add timestamp to average data
    average["timestamp"] = datetime.now(timezone.utc).strftime("%B %d, %Y at %I:%M %p (UTC)")
    
    # Save new average with its ID
    firebase_db.reference(f"{aquarium_id}/average/{new_id}").set(average)
    ref_latest_id.set(new_id)
    
    print(f"Daily average saved for aquarium {aquarium_id}: {average}")

def check_threshold(aquarium_id, sensors):
  ref = firebase_db.reference(f"{aquarium_id}/threshold")
  ref_notification = firebase_db.reference(f"{aquarium_id}/notification")
  notification = ref_notification.get()
  threshold = ref.get()
  
  if threshold is None:
    temporary_threshold = {
      "ph": {"min" : 0, "max" : 0 },
      "temperature": {"min" : 0, "max" : 0},
      "turbidity": {"min" : 0, "max" : 0}
    }
    ref.set(temporary_threshold)
  
  if notification is None:
    # Initialize individual notification channels with default False
    notification_settings = {
      "ph": False,
      "temperature": False,
      "turbidity": False
    }
    ref_notification.set(notification_settings)
    notification = notification_settings

  alerts = []   
  
  # Check pH threshold and notification setting
  if notification.get("ph", False) and (sensors["ph"] < threshold["ph"]["min"] or sensors["ph"] > threshold["ph"]["max"]):
    alerts.append("PH Alert")
  
  # Check temperature threshold and notification setting
  if notification.get("temperature", False) and (sensors["temperature"] < threshold["temperature"]["min"] or sensors["temperature"] > threshold["temperature"]["max"]):
    alerts.append("Temperature Alert")
  
  # Check turbidity threshold and notification setting
  if notification.get("turbidity", False) and (sensors["turbidity"] < threshold["turbidity"]["min"] or sensors["turbidity"] > threshold["turbidity"]["max"]):
    alerts.append("Turbidity Alert")

  if alerts:
    send_fcm_notification("Aquarium Alert", f"Aquarium {aquarium_id} {', '.join(alerts)}")

def calculate_daily_average(aquarium_id):
  ref = firebase_db.reference(f"{aquarium_id}/logs/latest_id")
  latest_id = ref.get()
  if latest_id is None:
    ref.set(0)
  
  ref = firebase_db.reference(f"{aquarium_id}/logs")
  pass



    
    
