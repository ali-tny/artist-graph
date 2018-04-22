import datetime
import urllib3

from bs4 import BeautifulSoup

from models import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_reviews(page=None, verbose=False, follow_links=True):
    artists = []
    albums = []
    reviews = []
    if page is None:
        url = 'http://pitchfork.com/reviews/albums/'
    else:
        url = 'http://pitchfork.com/reviews/albums/?page={}'.format(page)
    
    http_conn = urllib3.PoolManager()
    response = http_conn.request('GET', url)
    soup = BeautifulSoup(response.data, "html.parser")

    for review_list in soup.findAll('div', {'class':'infinite-container'}):
        for review_div in review_list.findAll('div', {'class': 'review'}):
            review_artists = review_div.find('ul', {'class':'artist-list review__title-artist'}).findAll('li')
            artist = ' & '.join(a.string for a in review_artists) # make one artist string in case of collab
            link = review_div.find('a')
            review_url = link['href']
            album = review_div.find('h2', {'class':'review__title-album'})
            album = album.string
            if verbose:
                print(artist, album)
            if follow_links:
                review = parse_review(http_conn, review_url)
            else:
                review = {}
            artists.append(artist)
            albums.append(album)
            reviews.append(review)
    return albums, artists, reviews
            
def parse_review(http_conn, url):
    response = http_conn.request('GET', 'http://pitchfork.com/'+url)
    soup = BeautifulSoup(response.data, "html.parser")
    body = soup.find('div', {'class':'contents dropcap'}).get_text() 
    rating = soup.find('span', {'class': 'score'}).get_text()
    standfirst = soup.find('div', {'class': 'review-detail__abstract'}).get_text()
    label = soup.find('li', {'class': 'labels-list__item'}).get_text()
    year = int(soup.find('span', {'class': 'single-album-tombstone__meta-year'}).get_text()[-4:])
    writer = soup.find('a', {'class': 'authors-detail__display-name'}).get_text()
    genre = soup.find('a', {'class': 'genre-list__link'})
    if genre:
        genre = genre.get_text()
    date = soup.find('time', {'class': 'pub-date'})['datetime']
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    except:
        date = None
    return dict(body=body, rating=rating, standfirst=standfirst,
                album_year=int(year), genre=genre, date=date,
                label=label, writer=writer)

