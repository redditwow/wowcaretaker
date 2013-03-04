from djcelery import celery
from syncer.models import (Subreddit, RedditGithubBranch, RedditGithubRepo, 
    GithubIP, Log)
from git import *
from praw import Reddit, errors
import os
from shutil import rmtree, copy2
from time import gmtime, strftime

import wowcaretaker.settings

r = wowcaretaker.settings.reddit

# This is a fucking rubbish library. I dont want you to
# fucking line-wrap my fucking content blocks. Fuck you.
# import scss
#
# fuck it, let's just use sass that we installed from ruby
# sure then we need more random ass shit on our prod environ
# but its worth the hassle since scss is a load of fucking
# horseshit
from subprocess import call

from syncer.models import RedditGithubBranch, Subreddit, RedditGithubRepo

# status images.
status_out_path = "/home/reddit/wchtml/status/"
status_in_path = "../../img/status/"
status_fileext = ".png"

# enables console logging for these functions
sdebug = True

def _status_update(subreddit, type_, progression):

    image_source = status_in_path + type_ + "/" + progression + status_fileext
    image_dest = status_out_path + subreddit + "-" + type_ + "-" + progression + status_fileext
    
    if not os.path.exists(status_out_path):
        try:
            os.makedirs(status_out_path)        
        except IOError as e:
            print e
            print "Could not update status images"
            return False

    try:
        copy2(image_source, image_dest)
    except:
        print "Some exception while copying a file"
        return False

    return True

def _get_repo_information(payload):

    url = payload['repository']['url']
    readonly_url = payload['repository']['url'].replace("https://", "git://") + ".git"
    branch = payload['ref'].replace("refs/heads/", "")
    head_commit = payload['head_commit']['id']

    return dict(url=url,
                readonly_url=readonly_url,
                branch=branch,
                head_commit=head_commit)

def compile_css(css_path, css_header):

    # lets try this again.
    css_temp_path = "/tmp/wcsyncer"

    # if our temp folder doesnt exist, create it
    if not os.path.exists(css_temp_path):
        try:
            os.makedirs(css_temp_path)        
        except IOError as e:
            print e

    # lets get less sassy. take our scss/sass/css files and
    # convert them to our temporary folder
    try:
        call(["sass", "--update", css_path+":"+css_temp_path])
    except:
        print "There was an error during call()"
    else:
        # assuming everything went ok, create a var to hold our new css.
        # include header as the top!
        compiled_css = css_header
        
        # and now the awesome part..
        for file in os.listdir(css_temp_path):
            if sdebug: print file
            css_data = open(css_temp_path + "/" + file, 'r').read()
            compiled_css += "\n" + css_data

        # delete the temp directory
        rmtree(css_temp_path)

        return compiled_css



    #raw_css = css_header

    #for file in os.listdir(css_path):
    #    if sdebug: print file
    #    css_file = open(css_path + "/" + file, 'r')
    #    css_data = css_file.read()
    #    css_file.close()
    #    raw_css += "\n" + css_data

    #_scss_vars = {}
    #_scss = scss.Scss(
    #    scss_vars=_scss_vars,
    #    scss_opts={
    #        'compress': False,
    #        'comments': True,
    #        'wrap': False,
    #    }
    #)    
    #if sdebug: print "_scss set..."
    #compiled_css = _scss.compile(raw_css)

    # lets code like a real motha fucka
    #call(["sass", "--update", css_path+":"+css_path+"/../roar"])

    #return compiled_css   


def pull_repo(readonly_url, url, branch):

    if sdebug: print "git pull from remote " + readonly_url
    
    # obtain the 
    repo = RedditGithubRepo.objects.get(url=url)
    branch = RedditGithubBranch.objects.get(repo=repo.pk, branch=branch)

    #print branch.name
    # just fucking around
    #for subreddit in  branch.subreddit.all():
    #    print "Destination Subreddit: ", subreddit

    repo_path = "../repo/{branch}".format(branch=branch.name)

    # make directories if they don't exist
    if not os.path.exists(repo_path):

        s = "Path for repo does not exist. Creating repo path: {repo_path}"
        print s.format(repo_path=repo_path)

        os.makedirs(repo_path)
        
        # the directory didnt exist which means we never created a git repo
        # (this is really bad practice, we should check for git, meh)
        
        try:
            repo = Repo.clone_from(readonly_url, repo_path)
        except:
            return False
        else:
            return True

    else:
        repo = Repo(repo_path).git.pull()
        return True    

@celery.task
def git_to_reddit(json_payload):

    if sdebug: print "git_to_reddit()"

    repo = _get_repo_information(json_payload)

    # first off. pull the fucking repo.
    repo_synced = pull_repo(repo['readonly_url'], repo['url'], repo['branch'])
    
    # grab the css, but first figure out which css :D
    
    if repo_synced:

        repo_db = RedditGithubRepo.objects.get(url=repo['url'])
        branch_db = RedditGithubBranch.objects.get(repo=repo_db.pk, branch=repo['branch'])
        

        repo_path = "../repo/{branch}".format(branch=branch_db.name)
        css_path = "{repo_path}/{css_path}".format(repo_path=repo_path, css_path=repo_db.css_folderpath)
        images_path = "{repo_path}/{images_path}".format(repo_path=repo_path, images_path=repo_db.images_folderpath)
        sidebar_file = "{repo_path}/{sidebar_filepath}".format(repo_path=repo_path, sidebar_filepath=repo_db.sidebar_filepath)
        
        print repo_path, "\n", css_path, "\n", images_path, "\n", sidebar_file, "\n"

        
        current_datetime = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        css_header = """ 
            /** This Stylesheet was automatically uploaded by the /r/wow bot
             **   It came from: {repo_url}
             ** Unix Timestamp: {datetime}
            """.format(repo_url=repo['url'], datetime=current_datetime)

        compiled_css = compile_css(css_path, css_header)
 
        #print compiled_css
        if sdebug: print "Opening my.css"
        temp = open('my.css', 'w+')
        temp.write(compiled_css)
        temp.close()
        if sdebug: print "Closing my.css"

        # upload the images, stylesheet and sidebar to reddit
        # and yes, it must be in that order to prevent BAD_CSS.
        for subreddit in branch_db.subreddit.all():
            srname = subreddit.name
            sr = r.get_subreddit(srname)

            for path, dirs, files in os.walk(images_path):
                for f in files:
                    curimg_path = path + "/" + f
                    try:
                        upload_image = sr.upload_image(image_path=curimg_path)
                        s = "{file} upload {status} to {srn}"

                    except (errors.APIException, errors.ClientException) as e:
                        print e
                        print s.format(file=f, status="failed",srn=srname)
                    else:
                        print s.format(file=f, status="successful",srn=srname)

            try:
                sr.set_stylesheet(compiled_css)
            except (errors.APIException, errors.ClientException) as e:
                print e
            else:
                if sdebug: print "Stylesheet Updated"

            sidebar_data = open(sidebar_file, 'r').read()
            try:
                sr.update_settings(description=sidebar_data)
            except (errors.APIException, errors.ClientException) as e:
                print e
            else:
                if sdebug: print "Sidebar Updated."
    
