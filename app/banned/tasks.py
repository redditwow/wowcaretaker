from djcelery import celery
from praw import Reddit, errors

# wowcaretaker specific
from banned.models import (Copypasta, ModReason, Url, YoutubeChannel, Phrase)
import wowcaretaker.settings as wcs
r = wcs.reddit
sdebug = wcs.DEBUG


def _debug_list_output(provided_list):

    if sdebug:
        for li in provided_list:
            print li


def _sdb_print(message):

    if sdebug:
        print message


def _get_banned_urls():

    banned_urls = Url.objects.all()

    _debug_list_output(banned_urls)

    return banned_urls


def _get_new_posts(subreddit, limit=100):

    try:
        sr = r.get_subreddit(subreddit)

    except (errors.APIException, errors.ClientException) as e:
        print e

    else:
        try:
            posts = sr.get_new(limit=limit)

        except (errors.APIException, errors.ClientException) as e:
            print e

        else:
            return posts

    return None


def _get_new_comments():
    # todo
    pass


def _remove_posts_with_urls(subreddit, num_posts=100):

    cur_post_id = 0
    posts = _get_new_posts(subreddit, limit=num_posts)
    urls = _get_banned_urls()
    debstrs = {
            'sburl': "Successfully replied to post with reason for banned url",
            'armurl': "post.url matches {url}. attempting to remove",
            'rmurlscs': "Successfully removed post with url {url}",
        }

    if posts is not None:
        for post in posts:
            cur_post_id += 1

            for url in urls:
               
                # really our urls should be stored as regex in the database
                # but this is just a lot simpler.
                # before this hack, urls with www. or another subdomain
                # or even https would not get removed.
                url.url = url.url.replace("http://", "")
                # best get rid of the trailing slash too, just incase.
                url.url = url.url.replace("/", "")

                if url.url in post.url:
                    _sdb_print(debstrs['armurl'].format(url=url.url))

                    try:
                        post.remove()

                    except (errors.APIException, errors.ClientException) as e:
                        print e

                    else:
                        _sdb_print(debstrs['rmurlscs'].format(url=url.url))

                        try:
                            post.add_comment(url.copypasta)

                        except (errors.APIException, 
                                errors.ClientException) as e:
                            print e
                        else:
                            _sdb_print(debstrs['sburl'])



# key = identifier string
# value = function to call
ACCEPTABLE_THINGS = {
        'urls' : _remove_posts_with_urls,
    }


@celery.task
def remove_banned_things(thing, subreddits=[], **kwargs):

    if thing not in ACCEPTABLE_THINGS:
        print "{thing} is not in ACCEPTABLE_THINGS".format(thing=thing)
    else:

        for subreddit in subreddits:
            print thing
            print subreddit
            print ACCEPTABLE_THINGS[thing]
            ACCEPTABLE_THINGS[thing](subreddit, **kwargs)
