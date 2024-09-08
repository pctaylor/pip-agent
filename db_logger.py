import logging
from datetime import datetime
from models import Session, UserAction, APICall, ErrorLog

class DatabaseLogger(logging.Handler):
    def emit(self, record):
        session = Session()
        try:
            if record.levelno == logging.ERROR:
                error_log = ErrorLog(
                    timestamp=datetime.utcnow(),
                    error_type=record.exc_info[0].__name__ if record.exc_info else 'Unknown',
                    error_message=record.getMessage(),
                    stack_trace=self.format(record),
                    session_id=getattr(record, 'session_id', None)
                )
                session.add(error_log)
            elif record.levelno == logging.INFO:
                if hasattr(record, 'action_type'):
                    user_action = UserAction(
                        session_id=getattr(record, 'session_id', None),
                        timestamp=datetime.utcnow(),
                        action_type=record.action_type,
                        prompt=getattr(record, 'prompt', None),
                        prompt_length=len(getattr(record, 'prompt', '')) if hasattr(record, 'prompt') else None,
                        response=getattr(record, 'response', None),  # New field
                        response_length=getattr(record, 'response_length', None),
                        response_time=getattr(record, 'response_time', None)
                    )
                    session.add(user_action)
            session.commit()
        finally:
            session.close()