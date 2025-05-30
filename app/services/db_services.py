from app.utils.firebase import firebase_db
from app.services.notification_service import send_fcm_notification
from datetime import datetime, timezone

def get_sensors(aquarium_id):
  ref = firebase_db.reference(f"{aquarium_id}/sensors")
  return ref.get()

def save_sensors(aquarium_id, sensors):
  ref_latest_id = firebase_db.reference(f"{aquarium_id}/logs/latest_id")
  latest_id = ref_latest_id.get()
  if latest_id is None:
    ref_latest_id.set(0)
  ref = firebase_db.reference(f"{aquarium_id}/sensors")
  ref.set(sensors)

def save_log_per_hour(aquarium_id, sensors):
    # Get latest log ID
    ref_latest_id = firebase_db.reference(f"{aquarium_id}/logs/latest_id")
    latest_id = ref_latest_id.get() or 0
    new_id = latest_id + 1

    # Save new hourly log
    firebase_db.reference(f"{aquarium_id}/logs/{new_id}").set(sensors)
    ref_latest_id.set(new_id)

    if new_id % 24 == 0:
        average = {
            "ph": 0,
            "temperature": 0,
            "turbidity": 0
        }
        logs = firebase_db.reference(f"{aquarium_id}/logs").get()
        if not logs:
            return

        ph_values, temp_values, turb_values = [], [], []

        for key, value in logs.items():
            if key.isdigit():
                ph_values.append(value["ph"])
                temp_values.append(value["temperature"])
                turb_values.append(value["turbidity"])

        if len(ph_values) > 0:  # Only calculate if we have values
            average["ph"] = round(sum(ph_values) / len(ph_values), 2)
            average["temperature"] = round(sum(temp_values) / len(temp_values), 2)
            average["turbidity"] = round(sum(turb_values) / len(turb_values), 2)

            average_per_day(aquarium_id, average)
             # Clear all logs except 'latest_id'
        logs_ref = firebase_db.reference(f"{aquarium_id}/logs")
        logs_ref.delete()

        # Reset latest_id to 0 for the next day
        ref_latest_id.set(0)

def average_per_day(aquarium_id, average):
    ref_latest_id = firebase_db.reference(f"{aquarium_id}/average/latest_id")
    latest_id = ref_latest_id.get() or 0
    new_id = latest_id + 1

    # Add timestamp to average data
    average["timestamp"] = datetime.now(timezone.utc).strftime("%B %d, %Y at %I:%M %p (UTC)")
    
    # Save new average with its ID
    firebase_db.reference(f"{aquarium_id}/average/{new_id}").set(average)
    ref_latest_id.set(new_id)

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
    ref_notification.set(False)

  if notification == True:
    alerts = []   
    
    if sensors["ph"] < threshold["ph"]["min"] or sensors["ph"] > threshold["ph"]["max"]:
      alerts.append("PH Alert")
    if sensors["temperature"] < threshold["temperature"]["min"] or sensors["temperature"] > threshold["temperature"]["max"]:
      alerts.append("Temperature Alert")
    if sensors["turbidity"] < threshold["turbidity"]["min"] or sensors["turbidity"] > threshold["turbidity"]["max"]:
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



    
    
