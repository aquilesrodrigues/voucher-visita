# from datetime import datetime
import datetime
from typing import List, Dict
import json
class DatetimeEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
      return obj.isoformat()
    return super().default(obj)
  