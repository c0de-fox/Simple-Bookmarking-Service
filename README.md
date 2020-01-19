# A simple bookmarking engine

This is a small python3 API and website that allows saving bookmarks into an SQLite3 database.

The production environment will eventually be hosted at [save.c0de.link](https://save.c0de.link)

## Completed Features:
* Database - Capable of any user-defined database file (multiple instances); Has Create/Read/Update/Delete methods for bookmarks

## Upcoming Features (TODO):
* Authentication - I'm thinking about using [Telethon](https://github.com/LonamiWebs/Telethon) which will send me auth tokens, which would then be sent along with the request
* Website UI - I want the website to be extremely easy to use. I plan on using [Bootstrap 4](https://getbootstrap.com/) with a style very similar to [lob.li](https://lob.li)
* API - Able to accept various HTTP methods (POST, GET for sure, possibly PUT and DELETE). This will interface with the database, and provide data sanitization. I'm planning on using [Bottle](https://bottlepy.org/docs/dev/) to accomplish this
* Chrome Extension - This will allow exporting bookmarks from Chrome into this service, as well as quickly adding pages, most likely through a right click menu and by clicking on the icon
* Firefox Extension - Everything the Chrome extension can do
