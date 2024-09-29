from enum import Enum

class NotificationType(Enum):
    GMAIL = "Gmail"
    MESSAGE = "Message"

class Website(Enum):
    JOBS_GE = "jobs.ge"
    HR_GE = "hr.ge"

class Frequency(Enum):
    EVERY_MINUTE = "Every minute"
    EVERY_HOUR = "Every hour"
    ONCE_A_DAY = "Once a day"

    @classmethod
    def to_minutes(cls, frequency):
        frequency_map = {
            cls.EVERY_MINUTE: 1,
            cls.EVERY_HOUR: 60,
            cls.ONCE_A_DAY: 1440,
        }
        return frequency_map[frequency]
