import os
from flask import Flask, request, render_template
from lib.database_connection import get_flask_database_connection
from lib.album_repository import AlbumRepository
from lib.album import Album
from lib.artist_repository import ArtistRepository
from lib.artist import Artist


# Create a new Flask app
app = Flask(__name__)

# The routes that are relevant to this task: 
# Get all albums and Get album by id

@app.route('/albums', methods=['GET'])
def get_albums():
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    albums = repository.all()
    
    return render_template("albums.html", albums=albums)

@app.route('/albums/<int:id>', methods=['GET'])
def get_album_by_id(id):
    connection = get_flask_database_connection(app)
    alb_repository = AlbumRepository(connection)
    try:
        album = alb_repository.find(id)
        art_repository = ArtistRepository(connection)
        artist = art_repository.find(album.artist_id)
    
        return render_template("album_show.html", album=album, artist=artist)

    except Exception as e:
        return render_template("album_error.html", error=str(e))


# Other, unrelated routes copied over from previous tasks

@app.route('/albums', methods=['POST'])
def create_album():
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    album = Album(
        None, 
        request.form['title'], 
        request.form['release_year'], 
        request.form['artist_id']
        )
    saved_album = repository.create(album)
    
    return ''

@app.route('/artists', methods=['GET'])
def get_artists():
    connection = get_flask_database_connection(app)
    repository = ArtistRepository(connection)
    artists = repository.all()
    return render_template("artists.html", artists=artists)

@app.route('/artists/<int:id>', methods=['GET'])
def get_artist_by_id(id):
    connection = get_flask_database_connection(app)
    art_repository = ArtistRepository(connection)
    try:
        print("Finding artist...")
        artist = art_repository.find(id)
        print("Artist found:", artist)

        alb_repository = AlbumRepository(connection)
        print("Finding albums...")
        albums = alb_repository.find_by_artist(id)
        print("Albums found:", albums)
    
        return render_template("artist_show.html", artist=artist, albums=albums)

    except Exception as e:
        return render_template("artist_error.html", error=str(e))

@app.route('/artists', methods=['POST'])
def post_artists():
    connection = get_flask_database_connection(app)
    repository = ArtistRepository(connection)
    artist = Artist(
        None,
        request.form['name'],
        request.form['genre']
    )
    saved_artist = repository.create(artist)
   
    return ''


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
