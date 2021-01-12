from sqlalchemy.orm import relationship
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from app import db
db = SQLAlchemy()


# Create Venue table
class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.JSON)  # modify the current Genres to be Json
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(255))
    website = db.Column(db.String(255))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text)
    artists = relationship('Artist', secondary='shows')
    shows = relationship('Show', backref="venues", lazy=True)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Venue {}>'.format(self.name)


# Create Artist table
class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.JSON)  # modify the current Genres to be Json
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(255))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(255))
    venues = relationship('Venue', secondary='shows')
    shows = relationship('Show', backref="artists", lazy=True)

    # CRUD
    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # def __repr__(self):
    #     return '<Artist %r>' % self
    def __repr__(self):
        return '<Artist {}>'.format(self.name)


# Create association table 'shows'
class Show(db.Model):
    __tablename__ = 'shows'

    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.now, primary_key=True)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Show {}{}>'.format(self.artist_id, self.venue_id)
