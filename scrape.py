from bs4 import BeautifulSoup
import urllib3

def get_reviews(page=None):
    artists = []
    albums = []
    reviews = []
    if page is None:
        url = 'http://pitchfork.com/reviews/albums/'
    else:
        url = 'http://pitchfork.com/reviews/albums/?page={}'.format(page)
    
    http_conn = urllib3.PoolManager()
    response = http_conn.request('GET', url)
    soup = BeautifulSoup(response.data)

    for review_list in soup.findAll('div', {'class':'infinite-container'}):
        for link in review_list('a'):
            review_url = link['href']
            artist = link.find('ul', {'class':'artist-list review__title-artist'})
            album = link.find('h2', {'class':'review__title-album'})
            if artist is None:
                continue
            artist = artist.string
            album = album.string
            review = parse_review(http_conn, review_url)
            artists.append(artist)
            albums.append(album)
            reviews.append(review)
    return albums, artists, reviews
            
def parse_review(http_conn, url):
    response = http_conn.request('GET', 'http://pitchfork.com/'+url)
    soup = BeautifulSoup(response.data)
    return soup.find('div', {'class':'contents dropcap'}).get_text() 
