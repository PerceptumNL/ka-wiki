import exercise_models
import gae_model
import khansync
import logging

class KhanSyncTest(gae_model.GAEModelTestCase):

    def setUp(self):
        super(KhanSyncTest, self).setUp(db_consistency_probability=1,
#            use_test_db=True,
#            test_db_filename='test_db.sqlite',
        )

    def test_repo_sync(self):
        sync = khansync.ExercisesSync()
        sync.sync()
        sync.sync_khan()
        exs = exercise_models.Exercise.all().fetch(1000)
        
    def test_exercise_topic(self):
        sync = khansync.ExercisesSync()
        sync.load_topictree()
        logging.error(sync.get_exercise_topic("absolute_value"))
