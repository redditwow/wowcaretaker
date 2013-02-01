from django.contrib import admin
from banned.models import Url, YoutubeChannel, Phrase, Copypasta, ModReason

class UrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'mod_reason')

admin.site.register(Url, UrlAdmin)
admin.site.register(YoutubeChannel)
admin.site.register(Phrase)
admin.site.register(Copypasta)
admin.site.register(ModReason)
