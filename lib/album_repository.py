from lib.album import Album
from lib.database_connection import DatabaseConnection
import psycopg

class AlbumRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * from albums')
        albums = []
        for row in rows:
            item = Album(
                row["id"], row["title"], row["release_year"], row["artist_id"]
                )
            albums.append(item)

        return albums
    
    def find(self, album_id):
        try:
            rows = self._connection.execute(
                'SELECT * from albums WHERE id = %s', [album_id]
                )
            row = rows[0]
            
            return Album(
                row['id'], row['title'], row['release_year'], row['artist_id']
            )

        except IndexError:
            raise Exception('No such ID')
        
    def find_by_artist(self, artist_id):
        try:
            rows = self._connection.execute(
                'SELECT * from albums WHERE artist_id = %s', [artist_id]
                )
            list_of_albums = [Album(
                row['id'], row['title'], row['release_year'], row['artist_id']
            ) for row in rows]

            return list_of_albums

        except IndexError:
            raise Exception('No such ID')
        
    def create(self, album):
        self._connection.execute(
            'INSERT INTO albums (title, release_year, artist_id) ' \
            'VALUES (%s, %s, %s)', [album.title, album.release_year, album.artist_id]
            )
        return None
    
