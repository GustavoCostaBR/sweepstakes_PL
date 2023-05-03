from datetime import datetime

date_str = '2023-04-08 00:00:00+00:00'
date_obj = datetime.fromisoformat(date_str)

day_month_str = date_obj.strftime('%d/%m')

print(day_month_str)
