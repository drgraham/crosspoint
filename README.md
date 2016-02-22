crosspoint.py
=============

Cross Point Church's [live streams](http://www.crosspoint.tv/internet/watch-live) use a service that supports HTML5, but the web app does not provide it to Firefox on Linux. This script extracts a url and passes it to vlc instead.

Requirements
------------

You will need [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/), [urllib3](https://urllib3.readthedocs.org/en/latest/), [PyGTK](http://www.pygtk.org/) (for error dialogs), [ImageMagick](http://www.imagemagick.org/script/index.php) (to install), and, of course, [vlc](http://www.videolan.org/vlc/index.html).

Install
-------

Run `make` to install in your `~/.local` directory. An icon and desktop file are also generated.
