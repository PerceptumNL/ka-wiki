import exercise_utils
import random
import unittest
from google.appengine.tools.dev_appserver import SetupStubs
from google.appengine.api import apiproxy_stub_map 
from google.appengine.api import datastore_file_stub 
#from google.appengine.api import mail_stub 
from google.appengine.api import urlfetch_stub


class TestExerciseUtils(unittest.TestCase):

    def setUp(self):
        SetupStubs("khan-panel", login_url="_ah/login", blobstore_path="/tmp", 
                    datastore_path="/tmp/khan_testdb.sqlite", clear_datastore=True, use_sqlite=True)

    def tearDown(self):
        pass

    def test_sync_exercises_from_repo(self):
        new_exs = exercise_utils.import_new_exercises_from_repo()
        self.assertTrue(len(new_exs) > 0)
        new_exs = exercise_utils.import_new_exercises_from_repo()
        self.assertTrue(len(new_exs)==0)
        updated_exs = exercise_utils.override_exercises_from_live()
        self.assertTrue(len(updated_exs) > 0)

    def test_sync_exercises_from_live(self):
        updated_exs = exercise_utils.override_exercises_from_live()
        self.assertTrue(len(updated_exs) == 0)

if __name__ == '__main__':
    unittest.main()
