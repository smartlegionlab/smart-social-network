from datetime import date


def calculate_age(date_of_birth):
    try:
        if date_of_birth:
            today = date.today()
            age = today.year - date_of_birth.year - (
                    (today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            return age
    except Exception as e:
        print(e)
        return None
