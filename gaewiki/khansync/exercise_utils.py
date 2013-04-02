import layer_cache
import urllib2
import logging
import json
import config
import git_repo
import setting_model
from exercise_models import Exercise
from google.appengine.ext import db


@layer_cache.cache_with_key_fxn(lambda *args, **kwargs:"raw_exercise_%s" % args[0])
def get_raw_exercise_from_git(name):
    url = config.exercises_url % name
    result = ""
    try:
        result = urllib2.urlopen(url).read()
        logging.info("get_git_exercises %s (%d bytes)" % (name, len(result)))
    except urllib2.URLError, e:
        logging.error(e)

    return result

def get_live_exercises():
    url = config.khan_domain + "/api/v1/exercises"
    result = ""
    try:
        result = urllib2.urlopen(url).read()
        logging.info("get_live_exercises from %s (%d bytes)" % (url, len(result)))
    except urllib2.URLError, e:
        logging.error(e)

    return json.loads(result)

#nice to be triggered when a topic tree update 
#and override only when is a *new exercise*
def override_exercises_from_live():
    live_exs = get_live_exercises()
    updated_exs = Exercise.update_from_jsonlist(live_exs)
    setting_model.Setting.exercises_last_update(update=True)
    return updated_exs

#to be trigger in any commit
#get file names from repository, and add them if doesn't exist
def import_new_exercises_from_repo():
    exs = git_repo.repo.get_exercises_list()
    stored_ex_names = [ex.name for ex in Exercise.all().fetch(99999)]
    new_exs = []
    for ex_name in exs:
        if not ex_name in stored_ex_names:
            logging.error("Add new exercise: %s" % ex_name)
            ex = Exercise(name=ex_name)
            new_exs.append(ex)
        else:
            logging.error("Already existing exercise: %s" % ex_name)
    db.put(new_exs)
    setting_model.Setting.exercises_last_update(update=True)
    return new_exs

def send_exercise_test(ex_name):
    ex = Exercise.get_by_name(ex_name)
    logging.info(ex)

