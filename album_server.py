import json

from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request


import album

@route("/albums/<artist>")
def albums(artist):
    albums_list, count_albums = album.find(artist)
    if not albums_list:
        message = f"Альбомов {artist} не найдено"
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = f"<h2>Количество альбомов {artist}: {str(count_albums)}</h2>"
        result += "<h3>Список альбомов:</h3>"
        result += "<br>".join(album_names)
    return result

@route("/albums", method="POST")
def albums():
    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    status_text = album.save_album(album_data)
    return status_text
if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)