from django.db import models

# Create your models here.

class Copypasta(models.Model):
    name = models.TextField(max_length=100)
    text = models.TextField(max_length=1000)

    def __unicode__(self):
        return self.name


class ModReason(models.Model):
    reason = models.TextField(max_length=200)

    def __unicode__(self):
        return self.reason


class Url(models.Model):
    url = models.URLField()
    mod_reason = models.ForeignKey(ModReason)
    copypasta = models.ForeignKey(Copypasta)

    def __unicode__(self):
        return self.url


class YoutubeChannel(models.Model):
    name = models.TextField()
    mod_reason = models.ForeignKey(ModReason)

    def __unicode__(self):
        return self.name


class Phrase(models.Model):
    phrase = models.TextField(max_length=1000)
    mod_reason = models.ForeignKey(ModReason)

    def __unicode__(self):
        return self.phrase