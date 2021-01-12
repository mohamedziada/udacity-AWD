# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from flask import Flask, render_template, request, Response, flash, redirect, url_for, session, logging
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy import func
import sys
import dateutil.parser
import babel
import json
import forgery_py

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
# done: connect to a local postgresql database
from models import Venue, Artist, Show

migrate = Migrate(app, db)


# Done: implement any missing fields, as a database migration using Flask-Migrate

# Done: implement any missing fields, as a database migration using Flask-Migrate

# Done: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
    # Done: replace with real venues data.
    data = []
    locations = Venue.query.with_entities(func.count(Venue.id), Venue.city, Venue.state) \
        .group_by(Venue.city, Venue.state).all()
    for location in locations:
        venue_data = []
        venues_locations = Venue.query.filter_by(state=location.state).filter_by(city=location.city).all()
        for venue in venues_locations:
            venue_data.append({
                "id": venue.id,
                "name": venue.name
            })
        data.append({
            "city": location.city,
            "state": location.state,
            "venues": venue_data
        })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
    # Search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    data = []
    results_response = {}
    search_term = request.form.get('search_term', '')
    search_result = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
    for result in search_result:
        num_shows = 0
        num_shows = len(
            db.session.query(Show).filter(Show.venue_id == result.id).filter(Show.start_time > datetime.now()).all())
        data.append({
            "id": result.id,
            "name": result.name,
            "num_upcoming_shows": num_shows,
        })
        results_response = {
            "count": len(search_result),
            "data": data
        }
    return render_template('pages/search_venues.html', results=results_response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # Done: replace with real venue data from the venues table, using venue_id
    up_shows = []
    past_shows = []
    venue = Venue.query.get(venue_id)  # get Venue by ID
    if not venue:  # if not exist render 404 page
        return render_template('errors/404.html')

    q_past_shows = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue_id).filter(
        Show.start_time < datetime.now()).all()

    for past_show in q_past_shows:
        past_shows.append({
            "artist_id": past_show.artist_id,
            "artist_image_link": past_show.artists.image_link,
            "artist_name": past_show.artists.name,
            "start_time": past_show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    q_upcoming_shows = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue_id).filter(
        Show.start_time > datetime.now()).all()

    for upcoming_show in q_upcoming_shows:
        up_shows.append({
            "artist_id": upcoming_show.artist_id,
            "artist_image_link": upcoming_show.artists.image_link,
            "start_time": upcoming_show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "artist_name": upcoming_show.artists.name
        })

    data = {  # prepare the Venue Json
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": up_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(up_shows),
    }
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # Done: insert form data as a new Venue record in the db, instead
    # Done: modify data to be the data object returned from db insertion
    error = False

    try:  # get request data
        venue = Venue(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            address=request.form['address'],
            phone=request.form['phone'],
            genres=request.form.getlist('genres'),
            facebook_link=request.form['facebook_link'],
            image_link=request.form['image_link'],
            website=request.form['website'],
            seeking_talent=True if 'seeking_talent' in request.form else False,
            seeking_description=request.form['seeking_description']
        )

        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        # done: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash(f'Venue {venue_id} was successfully deleted.')
    except:
        db.session.rollback()
        flash(f'An error occurred. Venue {venue_id} could not be deleted.')
    finally:
        db.session.close()

    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # Done: replace with real data returned from querying the database
    # data = [{
    #     "id": 4,
    #     "name": "Guns N Petals",
    # }, {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    # }, {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    # }]
    data = db.session.query(Artist).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
    # Search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    data = []
    search_q = request.form.get('search_term', '')
    search_results = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_q}%')).all()

    for search_result in search_results:
        data.append({
            "id": search_result.id,
            "name": search_result.name
        })

    # response = {
    #     "count": 1,
    #     "data": [{
    #         "id": 4,
    #         "name": "Guns N Petals"
    #     }]
    # }
    response = {
        "count": len(search_results),
        "data": data
    }

    return render_template('pages/search_artists.html', results=response, search_term=search_q)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # Done: replace with real venue data from the venues table, using venue_id
    data3 = {
        "id": 6,
        "name": "The Wild Sax Band",
        "genres": ["Jazz", "Classical"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "432-325-5432",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "past_shows": [],
        "upcoming_shows": [{
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-01T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-08T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-15T20:00:00.000Z"
        }],
        "past_shows_count": 0,
        "upcoming_shows_count": 3,
    }
    # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
    # artist = Artist.query.get(artist_id)
    # Retrieving artist  from database
    # print(artist.get_json)
    past_shows = []
    upcoming_shows = []
    artist = db.session.query(Artist).get(artist_id)

    if not artist:
        return render_template('errors/404.html')

    past_shows_q = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(
        Show.start_time > datetime.now()).all()

    for past_show in past_shows_q:
        past_shows.append({
            "venue_id": past_show.venue_id,
            "artist_image_link": past_show.venues.image_link,
            "venue_name": past_show.venues.name,
            "start_time": past_show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    upcoming_shows_q = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(
        Show.start_time < datetime.now()).all()

    for upcoming_show in upcoming_shows_q:
        upcoming_shows.append({
            "venue_id": upcoming_show.venue_id,
            "venue_name": upcoming_show.venues.name,
            "artist_image_link": upcoming_show.venues.image_link,
            "start_time": upcoming_show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    # artist = {
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo"
    # }
    # Done: populate form with fields from artist with ID <artist_id>
    artist = Artist.query.get(artist_id)

    if not artist:
        return render_template('errors/404.html')

    if artist:
        form.name.data = artist.name
        form.city.data = artist.city
        form.state.data = artist.state
        form.phone.data = artist.phone
        form.genres.data = artist.genres
        form.facebook_link.data = artist.facebook_link
        form.image_link.data = artist.image_link
        form.website.data = artist.website
        form.seeking_venue.data = artist.seeking_venue
        form.seeking_description.data = artist.seeking_description

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # done: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get(artist_id)

    if not artist:
        return render_template('errors/404.html')

    try:
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.genres = request.form.getlist('genres')
        artist.image_link = request.form['image_link']
        artist.facebook_link = request.form['facebook_link']
        artist.website = request.form['website']
        artist.seeking_venue = True if 'seeking_venue' in request.form else False
        artist.seeking_description = request.form['seeking_description']

        db.session.commit()
        flash('Artist was successfully updated!')

    except:
        flash('An error occurred. Artist could not be changed.')
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    # venue = {
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #     "address": "1015 Folsom Street",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "123-123-1234",
    #     "website": "https://www.themusicalhop.com",
    #     "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #     "seeking_talent": True,
    #     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #     "image_link": "https://images.unsplash.com/photo-15439006uto=format&fit=crop&w=400&q=60"
    # }
    # Done: populate form with values from venue with ID <venue_id>
    venue = Venue.query.get(venue_id)

    if not venue:
        return render_template('errors/404.html')

    if venue:
        form.name.data = venue.name
        form.city.data = venue.city
        form.state.data = venue.state
        form.phone.data = venue.phone
        form.address.data = venue.address
        form.genres.data = venue.genres
        form.facebook_link.data = venue.facebook_link
        form.image_link.data = venue.image_link
        form.website.data = venue.website
        form.seeking_talent.data = venue.seeking_talent
        form.seeking_description.data = venue.seeking_description

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # Done: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    venue = Venue.query.get(venue_id)

    if not venue:
        return render_template('errors/404.html')

    try:
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.genres = request.form.getlist('genres')
        venue.image_link = request.form['image_link']
        venue.facebook_link = request.form['facebook_link']
        venue.website = request.form['website']
        venue.seeking_talent = True if 'seeking_talent' in request.form else False
        venue.seeking_description = request.form['seeking_description']

        db.session.commit()
        flash(f'Venue was successfully updated!')
    except:
        flash(f'An error occurred. Venue could not be changed.')
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # Done: insert form data as a new Venue record in the db, instead
    # Done: modify data to be the data object returned from db insertion
    # Done: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')

    try:
        artist = Artist(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            phone=request.form['phone'],
            genres=request.form.getlist('genres'),
            facebook_link=request.form['facebook_link'],
            image_link=request.form['image_link'],
            website=request.form['website'],
            seeking_venue=True if 'seeking_venue' in request.form else False,
            seeking_description=request.form['seeking_description']
        )
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()


    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # done: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    data = []
    shows_q = db.session.query(Show).join(Artist).join(Venue).all()

    if not shows_q:
        return render_template('errors/404.html')

    for show_result in shows_q:
        data.append({
            "venue_id": show_result.venue_id,
            "venue_name": show_result.venues.name,
            "artist_id": show_result.artist_id,
            "artist_name": show_result.artists.name,
            "artist_image_link": show_result.artists.image_link,
            "start_time": show_result.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # done: insert form data as a new Show record in the db, instead
    # done: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    try:
        show = Show(
            artist_id=request.form['artist_id'],
            venue_id=request.form['venue_id'],
            start_time=request.form['start_time']
        )
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed')
    except:
        flash('An error occurred. Show could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


# ----------------------------------------------------------------------------#
# SEED.
# ----------------------------------------------------------------------------#
@app.cli.command(with_appcontext=False)
def seed():
    """Register CLI commands."""
    print(forgery_py.address.street_address())
    print(forgery_py.basic.frequency())
    print(forgery_py.email.subject())
    print(forgery_py.name.full_name())
    print(forgery_py.forgery.basic.boolean())
    print(forgery_py.forgery.name.company_name())
    print(forgery_py.forgery.lorem_ipsum.words(quantity=3, as_list=True))


# todo1 = TodoItem(...).save()
# todo2 = TodoItem(...).save()
# todo3 = TodoItem(...).save()
#    https://thispersondoesnotexist.com/image

# import forgery_py
# from random import randint
#
# for record in records:
#     todo = TodoItem(todo=forgery_py.lorem_ipsum.word(),
#                     due_date=forgery_py.date.date(),
#                     priority=randint(1, 4))
#     db.session.add(todo)
# try:
#     db.session.commit()
# except:
#     db.session.rollback()

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()