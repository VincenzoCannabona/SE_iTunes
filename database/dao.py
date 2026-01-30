from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod
    def get_all_album_duration(durata_minima):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a.id,a.title,a.artist_id, sum(milliseconds)/60000 as duration
                    FROM album a, track t
                    WHERE a.id=t.album_id
                    group by a.id, a.title, a.artist_id
                    having duration>%s"""

        cursor.execute(query, (durata_minima,))

        for row in cursor:
            album=Album(id=row["id"], title=row["title"],  artist_id=row["artist_id"], duration=row["duration"])
            result.append(album)
        cursor.close()
        conn.close()
        return result       #lista di oggetti Album

    @staticmethod
    def get_all_connessioni(durata_minima):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """with albumvalidi as (SELECT a.id, sum(milliseconds)/60000 as duration
                                        FROM album a, track t
                                        WHERE a.id=t.album_id
                                        group by a.id
                                        having duration>%s)
                    select distinct ab1.id as a1, ab2.id as a2
                    from albumvalidi ab1, albumvalidi ab2, track t1, playlist_track pt1, track t2, playlist_track pt2
                    where ab1.id = t1.album_id
                    and ab1.id < ab2.id
                    and ab2.id=t2.album_id
                    and t1.id=pt1.track_id
                    and t2.id=pt2.track_id
                    and pt1.playlist_id= pt2.playlist_id"""

        cursor.execute(query, (durata_minima,))

        for row in cursor:
            result.append((row["a1"], row["a2"]))
        cursor.close()
        conn.close()
        return result           #lista di tuple (id) di album collegati


