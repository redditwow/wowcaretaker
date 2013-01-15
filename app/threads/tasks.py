from celery.task import task
import wowcaretaker.settings as settings

print "LOLOLOL"
reddit = settings.reddit
print reddit

#try: 
#    reddit.submit("fluxflashor", "celery test", "yarr harrr")
#except errors.APIException as e:
#    print e

@task
def create_thread(subreddit, thread_title, thread_text):
    print "CREATE_THREAD IS RUNNING"
    sr = reddit.get_subreddit(subreddit)
    posts = sr.get_hot(limit=100)

    for post in posts:
        print post

    reddit.submit(subreddit, thread_title, thread_text)

    return "Thread"