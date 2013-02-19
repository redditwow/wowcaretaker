from djcelery import celery
from syncer.models import Subreddit, RedditGithubBranch, RedditGithubRepo, GithubIP, Log
from git import *
import praw as reddit
import os

from syncer.models import RedditGithubBranch, Subreddit, RedditGithubRepo

# enables console logging for these functions
sdebug = True

def _get_repo_information(payload):
    url = payload['repository']['url']
    readonly_url = payload['repository']['url'].replace("https://", "git://") + ".git"
    branch = payload['refs'].replace("refs/heads/")
    head_commit = payload['head_commit']['id']

    return dict(url=url,
                readonly_url=readonly_url,
                branch=branch,
                head_commit=head_commit)

def pull_repo(readonly_url, url, branch):

    if sdebug: print "git pull from remote " + readonly_url
    
    # obtain the 
    repo = RedditGuthubRepo.objects.get(url=url)
    branch = RedditGithubBranch.objects.get(repo=repo.pk, branch=branch)

    print repo.name



@celery.task
def git_to_reddit(json_payload):
    if sdebug: print "git_to_reddit()"

    repo = _get_repo_information(json_payload)

    # first off. pull the fucking repo.
    repo_synced = pull_repo(repo.readonly_url, repo.url)
    