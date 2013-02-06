from django.db import models

# contains all of the ips we want to accept post data from
# storing these in the database may increase processing
# slightly, but it's worth it since we don't need to make
# code changes when github decides to go crazy.
class GithubIP(models.Model):
    ip_address = models.IPAddressField()

    def __unicode__(self):
        return self.ip_address


# stores important information about our github repos
class RedditGithubRepo(models.Model):
    url = models.UrlField(primary_key=True)

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
    branch = models.TextField()

    def __unicode__(self):
        return self.name

# all subreddits need a branch
class Subreddit(models.Model):
    name = models.TextField(primary_key=True)
    branch = models.ForeignKey(GithubBranch)

    def __unicode__(self):
        return self.name