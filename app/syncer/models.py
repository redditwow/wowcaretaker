from django.db import models

# contains all of the ips we want to accept post data from
# storing these in the database may increase processing
# slightly, but it's worth it since we don't need to make
# code changes when github decides to go crazy.
class GithubIP(models.Model):
    ip_address = models.IPAddressField()

    def __unicode__(self):
        return self.ip_address


class Subreddit(models.Model):
    name = models.TextField(primary_key=True)

    def __unicode__(self):
        return self.name


# stores important information about our github repos
class RedditGithubRepo(models.Model):
    url = models.URLField(unique=True)

    # very important reddit configuration stuff.
    # this could all be hardcoded but why limit ourselves?
    css_folderpath = models.TextField()
    images_folderpath = models.TextField()
    sidebar_filepath = models.TextField()
    description_filepath = models.TextField()

    def __unicode__(self):
        return self.url


# stores our github branch data. will let us sync
# different branches to different subreddits
class RedditGithubBranch(models.Model):
    name = models.TextField(primary_key=True) # retard proof.. hopefully
    repo = models.ForeignKey(RedditGithubRepo)
    branch = models.TextField()
    subreddit = models.ForeignKey(Subreddit)

    def __unicode__(self):
        return self.name


# simple syncer log
class Log(models.Model):
    timestamp = models.DateTimeField('date published')
    entry = models.TextField(max_length=2000)

    def __unicode__(self):
        return self.entry
