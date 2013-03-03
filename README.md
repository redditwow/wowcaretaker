wowcaretaker
============

Our friendly robot that takes care of moderation and menial tasks for the wow subreddit, and it's sisters, on reddit.com

This bot was designed to make life super simple for the moderators and will eventually let us do some pretty crazy shit. Since it is backed by a database and web interface, we can add new rules to the bot for moderation without any code changes.

What does it do?
================

Currently the bot supports syncing the css, images, and sidebar data from github to reddit.

Eventually it will include:

* Rules system for removal of stuff
* IRC taskqueue integration

Requirements
============

The following are required to run this hack of a bot. Everything should work with up to date packages, and if it doesn't, get owned? Nah just let [me](http://github.com/fluxflashor) know something has gone funky and I'll look into it.

Ruby Gems

* SASS (called from python)

Python Packages

* celery
* django
* django-celery
* simplejson
* praw
* pythongit

Other stuff

* A database to store data in (seriously.)
* A reddit.com account with FULL moderator permissions for the subreddit(s) the bot will be moderating
* [Optional] Webserver to proxy the django cgi