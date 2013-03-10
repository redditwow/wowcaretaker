wowcaretaker
============

Our friendly robot that takes care of moderation and menial tasks for the wow subreddit, and it's sisters, on reddit.com

This bot was designed to make life super simple for the moderators and will eventually let us do some pretty crazy shit. Since it is backed by a database and web interface, we can add new rules to the bot for moderation without any code changes.

System Status
=================================

| Subreddit     | Status                                      |||
| ------------- |:-------------:|:-------------:|:-------------:|
| **/r/wow**    | [![wowcssstatus][wowcssstatus]][wowcssstatus] | [![wowimgstatus][wowimgstatus]][wowimgstatus] | [![wowsdbstatus][wowsdbstatus]][wowsdbstatus] |
| **/r/woweconomy**    | [![woweconomycssstatus][woweconomycssstatus]][woweconomycssstatus] | [![woweconomyimgstatus][woweconomyimgstatus]][woweconomyimgstatus] | [![woweconomysdbstatus][woweconomysdbstatus]][woweconomysdbstatus] |
| **/r/wowstreams**    | [![wowstreamscssstatus][wowstreamscssstatus]][wowstreamscssstatus] | [![wowstreamsimgstatus][wowstreamsimgstatus]][wowstreamsimgstatus] | [![wowstreamssdbstatus][wowstreamssdbstatus]][wowstreamssdbstatus] |
| **/r/multiboxing**    | [![multiboxingcssstatus][multiboxingcssstatus]][multiboxingcssstatus] | [![multiboxingimgstatus][multiboxingimgstatus]][multiboxingimgstatus] | [![multiboxingsdbstatus][multiboxingsdbstatus]][multiboxingsdbstatus] |


[wowcssstatus]: https://battletagfriendfinder.com/sync-status/wow-css.png
[wowimgstatus]: https://battletagfriendfinder.com/sync-status/wow-images.png
[wowsdbstatus]: https://battletagfriendfinder.com/sync-status/wow-sidebar.png
[woweconomycssstatus]: https://battletagfriendfinder.com/sync-status/woweconomy-css.png
[woweconomyimgstatus]: https://battletagfriendfinder.com/sync-status/woweconomy-images.png
[woweconomysdbstatus]: https://battletagfriendfinder.com/sync-status/woweconomy-sidebar.png
[wowstreamscssstatus]: https://battletagfriendfinder.com/sync-status/wowstreams-css.png
[wowstreamsimgstatus]: https://battletagfriendfinder.com/sync-status/wowstreams-images.png
[wowstreamssdbstatus]: https://battletagfriendfinder.com/sync-status/wowstreams-sidebar.png
[multiboxingcssstatus]: https://battletagfriendfinder.com/sync-status/multiboxing-css.png
[multiboxingimgstatus]: https://battletagfriendfinder.com/sync-status/multiboxing-images.png
[multiboxingsdbstatus]: https://battletagfriendfinder.com/sync-status/multiboxing-sidebar.png

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