from django.db import models

class RepoType(models.Model):
    type = models.TextField()

    def __unicode__(self):
        return self.type


class GithubIP(models.Model):
    ip_address = models.IPAddressField()

    def __unicode__(self):
        return self.ip_address


class GithubRepo(models.Model):
    name = models.TextField()
    url = models.TextField()
    type = models.ForeignKey(RepoType)

    def __unicode__(self):
        return self.name


class Subreddit(models.Model):
    subreddit_name = models.TextField(primary_key=True)
    subreddit_repo = models.ForeignKey(GithubRepo)

    def __unicode__(self):
        return self.subreddit_name


class RedditAccount(models.Model):
    username = models.TextField()
    password = models.TextField()

    def __unicode__(self):
        return self.username