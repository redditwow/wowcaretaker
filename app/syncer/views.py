from django.http import HttpResponse, Http404
from django.template import RequestContext, Context, loader
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from syncer.models import Subreddit, GithubIP
import simplejson as json

import urllib2
import ipaddr

import syncer.tasks

api_url = "https://api.github.com/"

def gh_api_req(path):

    try:
        request_data = urllib2.urlopen(api_url+path).read()
    except urllib2.HTTPError, e:
        print "HTTP Error: %d" % e.code
    return json.loads(request_data)


def _is_github_ip(ip):

    meta = gh_api_req("meta")

    for ipcidr in meta['hooks']:
    
        if ipaddr.IPAddress(ip) in ipaddr.IPNetwork(ipcidr):
            return True

    else:
        return False


@csrf_exempt
def subreddit(request, subreddit):

    request_ip = request.META["REMOTE_ADDR"]

    if request.method=="POST":

        request_is_valid  = _is_github_ip(request_ip)

        if request_is_valid:

            try:
                github_payload = json.loads(request.POST['payload'])

            except:
                print "Request made from {ip} was valid but payload was not submitted.".format(ip=request_ip)
                return HttpResponse("Please submit a payload.")

            else:
                print "Request made from {ip} was valid and contained a payload".format(ip=request_ip)

                # make sure the repo is in our allowed list


                # figure out which branch it was using

                # a valid request with payload means we need to call a task
                syncer.tasks.git_to_reddit.delay(github_payload)

                return HttpResponse("Thank you for your payload ;)")

        else:
            print "Request made from {ip} is not in our whitelist.".format(ip=request_ip)
            return HttpResponse("You are not allowed to POST data to this area.")

    else:
        print "Request made from {ip} did not submit POST data.".format(ip=request_ip)

        return HttpResponse("Hello")
