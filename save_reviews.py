from scrape import get_reviews
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import AlbumReview, Artist

def get_existing_artist_ids(session, artist_list):
    # return dict of artist_name: artist_id mappings for artists in artist_list
    artist_ids = []
    query = session.query(Artist.id, Artist.name).filter(Artist.name.in_(artist_list))
    results = query.all()
    name2id = {r[1]: r[0] for r in results}
    return name2id

def review_exists(session, review_dict):
    # (alt soln: https://stackoverflow.com/questions/44511046/sqlalchemy-prevent-duplicate-rows)
                
    alb_q = session.query(AlbumReview.id).filter(AlbumReview.artist_id == review_dict['artist_id'],
                                                 AlbumReview.album_title == review_dict['album_title'])
    alb_q = session.query(alb_q.exists()).scalar()
    return alb_q

if __name__ == '__main__':

    engine = create_engine('sqlite:///pitchfork_example.db') # to connect to e.g. remote d.b. just change url here
    Session = sessionmaker(bind=engine)
    session = Session()
    
    for page in [1]:
        album_reviews = []
        new_artists = {}
        albums, artists, reviews = get_reviews(page, verbose=True)
        name2id = get_existing_artist_ids(session, artists)
        for artist, album, review in zip(artists, albums, reviews):
            # print(artist, album)
            artist_id = name2id.get(artist)
            review['album_title'] = album
            if artist_id:
                review['artist_id'] = artist_id
                # check for already existing review in db 
                if review_exists(session, review):
                    print('existing review for {}: {}, skipping'.format(artist, album))
                    continue
            else:
                # hopefully maintaining a single object per new artist to created
                # prevents duplicates being created? 
                if artist in new_artists:
                    review['artist'] = new_artists['artist']
                else:
                    review['artist'] = Artist(name=artist)
                    new_artists['artist'] = Artist
                
            album_reviews.append(AlbumReview(**review))
        session.add_all(album_reviews)
        session.commit()

