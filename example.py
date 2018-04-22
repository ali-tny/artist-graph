from scrape import get_reviews

for page in [1,2,3]:
    # should write these to a DB or something
    artists, albums, reviews = get_reviews(page)

print(artists)
print(albums)
print(reviews)