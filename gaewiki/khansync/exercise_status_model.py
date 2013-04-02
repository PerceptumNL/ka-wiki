
from exercise_model import Exercise

class _STATUS():
    UNTESTED = "untested"
    WORKING = "working"
    BROKEN = "broken"

class ExerciseStatus(backup_model.BackupModel):
    """Information about a single user's interaction with a single exercise."""
    user = db.UserProperty()
    exercise_model = db.ReferenceProperty(Exercise)
    status = db.StringProperty(default=_STATUS.UNTESTED)

    @staticmethod
    def insert_status(user, exercise_name, status):
        ex = Exercise.get_by_name(exercise_name)
        ExerciseStatus()
        
