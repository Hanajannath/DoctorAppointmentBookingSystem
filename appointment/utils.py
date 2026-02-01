from datetime import date, datetime

def is_past_time(selected_date, selected_slot):
    """
    selected_slot example: '02:00 PM - 03:00 PM'
    """
    try:
        slot_start_str = selected_slot.split('-')[0].strip()
        slot_start_time = datetime.strptime(slot_start_str, "%I:%M %p").time()

        selected_datetime = datetime.combine(
            date.fromisoformat(selected_date),
            slot_start_time
        )

        return selected_datetime < datetime.now()
    except:
        return True

def slot_within_doctor_time(slot, doctor_time):
    """
    slot: '09-10'
    doctor_time: '09:00 AM - 04:00 PM'
    """
    try:
        slot_start_hour, slot_end_hour = map(int, slot.split('-'))

        doc_start, doc_end = doctor_time.split(' - ')
        doc_start_hour = datetime.strptime(doc_start, "%I:%M %p").hour
        doc_end_hour = datetime.strptime(doc_end, "%I:%M %p").hour

        return doc_start_hour <= slot_start_hour and slot_end_hour <= doc_end_hour
    except Exception as e:
        print("TIME ERROR:", e)
        return False