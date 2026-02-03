from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod
    def get_album_by_durata(durata):
        conn = DBConnect.get_connection()

        result = []

        # trovare coppie album (id) durata
        # vedere quale durata soddisfa
        # prendere tutti le info di album
        cursor = conn.cursor(dictionary=True)
        query = """select t.album_id as id , a.title, a.artist_id,t.durata
                    from (SELECT album_id, sum(milliseconds)/60000 as durata
                        from track t
                        group by album_id) as t, album a
                    where t.album_id = a.id and durata>%s """

        cursor.execute(query, (durata,))

        for row in cursor:
            album=Album(**row)
            result.append(album)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_collegamenti(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        #trovare traccie appartenenti a ciscun album
        #controllare stessa playlst se ci sono traccie in comune
        query = """with album_filtrati as (select t.album_id as id , a.title, a.artist_id,t.durata
                                            from (SELECT album_id, sum(milliseconds)/60000 as durata
                                            from track t
                                            group by album_id) as t, album a
                                            where t.album_id = a.id and durata>%s)
                    select af1.id as a1, af2.id as a2
                    from album_filtrati af1, album_filtrati af2, track t1,track t2, playlist_track p1, playlist_track p2
                    where af1.id=t1.album_id 
                    and af2.id=t2.album_id 
                    and af1.id<af2.id
                    and t1.id=p1.track_id
                    and t2.id=p2.track_id
                    and p1.playlist_id=p2.playlist_id
                    group by af1.id, af2.id """

        cursor.execute(query, (durata,))

        for row in cursor:
            result.append((row['a1'], row['a2']))

        cursor.close()
        conn.close()
        return result

