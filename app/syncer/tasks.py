from djcelery import celery
from syncer.models import Subreddit
from git import *
import praw as reddit
import os

# note: bunch of stuff in here is for debug purposes to log to the main django console.
# it isn't pretty but it works. one day there will be a better handler for this stuff.

@celery.task
def pull_repo(subreddit, git_url):
    print "Request to pull git data for /r/:" + subreddit

    # get the repo url for this subreddit
    sr = Subreddit.objects.get(subreddit_name=subreddit)
    url = sr.subreddit_repo.url

    if git_url is url:
        print "The url from git matches our url in the database"

        # our repos are going to be stored locally inside of the 'repo' folder
        # wowcaretaker/repo/**subreddit**

        repo_path = "../../repo/" + subreddit

        # we are doing a bit of assuming here which is bad.
        # if the path exists, we just assume it's a repo.
        # this is poor programming.
        if not os.path.exists(repo_path):
            print "The repo does not exist"

            try:
                os.makedirs(repo_path)
            except:
                print "Unable to create directory for repo"
            else:
                # lets get the read-only url to pull from
                remote = git_url.replace("https://", "git://") + ".git"

                # and finally create a local version of the repo
                repo = Repo.clone_from(remote, repo_path)

        else:
            print "The repo exists."
            repo = Repo(repo_path)
            repo.git.pull()

        # we have our repo data, let's do something with it


    else:
        print "The url from git does not match our url in the database"
        pass
