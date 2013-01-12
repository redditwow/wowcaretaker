from django.contrib import admin
from syncer.models import RepoType, GithubIP, GithubRepo, Subreddit, RedditAccount

admin.site.register(RepoType)
admin.site.register(GithubIP)
admin.site.register(GithubRepo)
admin.site.register(Subreddit)
admin.site.register(RedditAccount)
