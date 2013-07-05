
#Github sync
from secrets import *
from github import Github
from exercise_models import Exercise
import logging
import urllib
import json

def get_repo_html_exercises():
    g = Github(github_user, github_password)
    u = g.get_user()
    r = g.get_repo(github_repo)
    b = r.get_branch(github_branch)
    sha = b.commit.sha
    ex_files = [f.name for f in r.get_dir_contents("/khan-exercises/exercises", sha) if "html" in f.name]
    return ex_files


class ExercisesSync():
    exs = []
    ex_db_files = []
    topictree = None

    def __init__(self):
        self.exs = Exercise.all().fetch(9999)
        self.ex_db_files = [ex.file_name for ex in self.exs]

    def load_topictree(self):
        f = urllib.urlopen(khan_domain + "/api/v1/topictree")
        self.topictree = json.load(f)

    def get_exercise_topic(self, exercise_name):
        def find_topics(children, topics=[]):
            for child in children:
                if child['kind'] == "Exercise" and child['name'] == exercise_name:
                    return topics
                elif child['kind'] == "Topic":
                    topics_copy = list(topics)
                    topics_copy.append(child['standalone_title'])
                    ret = find_topics(child['children'], topics_copy)
                    if ret: return ret
                else:
                    continue
            return False
        
        topics = find_topics(self.topictree['children'])
        if topics: return topics
        else: return []

    def sync(self):
        self.sync_repo()
        self.load_topictree()
        self.sync_khan()

    def sync_repo(self):
        ex_repo_files = get_repo_html_exercises()
        for repo_file in ex_repo_files:
            if not repo_file in self.ex_db_files:
                newex = Exercise(name=repo_file.replace(".html",""), file_name=repo_file)
                newex.live = False
                newex.put()
                logging.error("Add exercise from repo: %s" % repo_file)
        self.exs = Exercise.all().fetch(9999)
        self.ex_db_files = [ex.file_name for ex in self.exs]
        return True
    
    def sync_khan(self):
        #params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
        f = urllib.urlopen(khan_domain + "/api/v1/exercises")
        live_exs = json.load(f)
        for ex in live_exs:
            ex_file = ex['name'] + ".html"
            if ex_file in self.ex_db_files:
                ex_db = Exercise.get_by_name(ex['name'])
                ex_db.file_name = ex_file
                ex_db.description = ex['description']
                ex_db.pretty_display_name = ex['pretty_display_name']
                ex_db.short_display_name = ex['short_display_name']
                ex_db.tags = ex['tags']
                ex_db.live = True
                ex_db.topics = self.get_exercise_topic(ex['name'])
                ex_db.put()
            else:
                logging.error("Exercise out of sync: %s" % ex_file)
