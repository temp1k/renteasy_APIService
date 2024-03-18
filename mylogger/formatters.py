from datetime import datetime

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):

    def __init__(self):
        super(CustomJsonFormatter, self).__init__()
        self.json_ensure_ascii = False

    def add_fields(self, log_record, record, message_dict):
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now

        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
