from sqlalchemy import Column, Integer, String, ForeignKey, Text,\
                       Numeric, Date, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Artist(Base):
  __tablename__ = 'artists'
  id = Column(Integer, primary_key=True) #TODO maybe actually use some kind of open data id as pk
  name = Column(String)
  album_reviews = relationship("AlbumReview", backref="artist") # establishes a two way relationship (artist.album_reviews, albumreview.artist)

# class Album(Base):
#   __tablename__ = 'albums'
#   id = Column(Integer, primary_key=True) #TODO maybe actually use some kind of open data id as pk
#   title = Column(String)
#   reviews = relationship("AlbumReview", backref="album")
#   year = Column(Integer)
#   label = Column(String(20), nullable=True)
#   artist_id = Column(Integer, ForeignKey('artists.id'), nullable=True)
  # year

class AlbumReview(Base):
  """
  From sqlalchemy docs: A class using Declarative at a minimum needs 
  a __tablename__ attribute, and at least one Column which is part of a primary key
  """
  __tablename__ = 'album_reviews'
  id = Column(Integer, primary_key=True)
  rating = Column(Numeric(precision=2), nullable=True)
  genre = Column(String(20), nullable=True)
  writer = Column(String(20), nullable=True)
  label = Column(String(20), nullable=True)
  album_title = Column(String(20))
  album_year = Column(Integer)
  label = Column(String(20), nullable=True)
  body = Column(Text)
  standfirst = Column(Text, nullable=True)
  date = Column(Date, nullable=True)
  artist_id = Column(Integer, ForeignKey('artists.id'), nullable=True)
  # TODO index and unique together artist id album title

  def __repr__(self):
    return "<Review(artist='{}', album='{}')".format(
                  self.artist.name, self.album_title)

if __name__ == '__main__':
  engine = create_engine('sqlite:///pitchfork_example.db')
  Base.metadata.create_all(engine) # creates tables - will not overwrite or delete them
