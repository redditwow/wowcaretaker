from django.contrib import admin
from syncer.models import GithubIP, RedditGithubRepo, RedditGithubBranch, Subreddit, Log

admin.site.register(GithubIP)
admin.site.register(RedditGithubRepo)
admin.site.register(RedditGithubBranch)
admin.site.register(Subreddit)
admin.site.register(Log)
