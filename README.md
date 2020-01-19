# A simple bookmarking engine

This is a small python3 API and website that allows saving bookmarks into an SQLite3 database.

The production environment will eventually be hosted at [save.c0de.link](https://save.c0de.link)

## Usage

This project uses [Pipenv](https://pipenv.readthedocs.io/en/latest/) to manage the dependencies, so install that first after cloning this repository.

* Install dependencies - `pipenv install`
* Enter the environment - `pipenv shell`
* Start the server - `python server.py`

The server will be running on `http://localhost:8080/`

## Available Requests

Now that you have a running server, you can issue requests via a web browser, curl, wget, etc to the following endpoints:

* `/` - Currently returns the string "This is the index"
* `/save/<title>/<uri>` - Creates a new bookmark entry for the provided `uri`. `title` is a human readable word/set of words to recognize saved bookmarks quickly. Returns a JSON object containing the `uuid`
* `/get/all` or `/getall` - Returns a JSON object containing all bookmarks saved, or a 404 error if there are none
* `/get/<uuid>` - Returns a JSON object containing the bookmark. `uuid` is a UUID that is returned from `/save`, `/get/all` and `/get/<uuid>`
* `/delete/<uuid>` - Returns a JSON object containing the `uuid` and deletion status. Deletes the bookmark. `uuid` is a UUID that is returned from `/save`, `/get/all` and `/get/<uuid>`
* `/update/title/<uuid>/<title>` - Changes the bookmark's `title` with the newly provided one. Returns the same bookmark object as `/get/<uuid>`. `uuid` is a UUID that is returned from `/save`, `/get/all` and `/get/<uuid>`
* `/update/uri/<uuid>/<uri>` - Changes the bookmark's `uri` with the newly provided one. Returns the same bookmark object as `/get/<uuid>`. `uuid` is a UUID that is returned from `/save`, `/get/all` and `/get/<uuid>`. By design, the bookmark's `uuid` will be updated. If the updated `uuid` is already in the database, an HTTP 409 Conflict will be raised.

## The Bookmark Object

The following fields will be returned with `/get` and `/update` requests:

* `uuid` - Required (generated automatically) - This is used for `/get`, `/update` and `/delete` requests
    * This is regnerated when updating the URI due to the fact that it is based on the URI of the bookmark
    * This is generated with the following criteria:
    ```
    Generate a UUID based on the SHA-1 hash of the python URL namespace identifier
    (which is 6ba7b811-9dad-11d1-80b4-00c04fd430c8) and a uri (which is a string)
    ```
* `uri` - Required (user provided) - This is a full link. Currently the API does not verify that it is reachable, so it can be any form of URI, including [UNC Paths](https://en.wikipedia.org/wiki/Path_(computing)#UNC), or even a bare string
* `title` - Required (user provided) - A human readable word/set of words to recognize saved bookmarks quickly
* `date_created` - Required (generated automatically) - This is the date and time of the server when the request was received to save a bookmark
* `date_updated` - Optional (generated automatically) - This is the date and time of the server when the request was received to update a bookmark

### Completed Features:
* Database - Capable of any user-defined database file (multiple instances); Has Create/Read/Update/Delete methods for bookmarks
* API - All of the features in the database have been implemented in the API (currently unauthenticated and unsanitized and everything is GET Requests) - Uses [Bottle](https://bottlepy.org/docs/dev/)

### Features In Progress:
* Authentication - Uses [Telethon](https://github.com/LonamiWebs/Telethon) to provide me with an API key

### Upcoming Features (TODO):
* ~~Authentication - I'm thinking about using [Telethon](https://github.com/LonamiWebs/Telethon) which will send me auth tokens, which would then be sent along with the request~~
* Website UI - I want the website to be extremely easy to use. I plan on using [Bootstrap 4](https://getbootstrap.com/) with a style very similar to [lob.li](https://lob.li)
* ~~API - Able to accept various HTTP methods (POST, GET for sure, possibly PUT and DELETE). This will interface with the database, and provide data sanitization. I'm planning on using [Bottle](https://bottlepy.org/docs/dev/) to accomplish this~~
    * Fetch various meta-data from the URI if it is reachable
        * HTML title, favicon, etc
    * Determine if a link is reachable
* Chrome Extension - This will allow exporting bookmarks from Chrome into this service, as well as quickly adding pages, most likely through a right click menu and by clicking on the icon
* Firefox Extension - Everything the Chrome extension can do
