from enum import Enum

class NotificationType(Enum):
    GMAIL = "Gmail"
    MESSAGE = "Message"

class Website(Enum):
    JOBS_GE = "jobs.ge"
    HR_GE = "hr.ge"

class Frequency(Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    
    @classmethod
    def to_minutes(cls, frequency):
        frequency_map = {
            cls.DAILY: 1440,   
            cls.WEEKLY: 10080, 
            cls.MONTHLY: 43200
        }
        return frequency_map.get(frequency, None) 