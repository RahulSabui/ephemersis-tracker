from flask import Flask, render_template, request, jsonify
from skyfield.api import load, Topos, utc
from datetime import datetime

app = Flask(__name__)

def get_planetary_positions(dob_str, latitude, longitude):
    eph = load('de421.bsp')
    ts = load.timescale()
    dob = datetime.strptime(dob_str, "%Y-%m-%d %H:%M").replace(tzinfo=utc)
    t = ts.utc(dob)

    observer = Topos(latitude_degrees=latitude, longitude_degrees=longitude)
    earth = eph['earth']

    bodies = {
        'Sun ☀': eph['sun'],
        'Moon 🌕': eph['moon'],
        'Mercury 🜍': eph['mercury'],
        'Venus ♀': eph['venus'],
        'Mars ♂': eph['mars'],
        'Jupiter ♃': eph['jupiter barycenter'],
        'Saturn ♄': eph['saturn barycenter'],
        'Uranus ♅': eph['uranus barycenter'],
        'Neptune ♆': eph['neptune barycenter'],
        'Pluto ♇': eph['pluto barycenter'],
    }

    positions = []
    for name, body in bodies.items():
        astrometric = (earth + observer).at(t).observe(body).apparent()
        ra, dec, distance = astrometric.radec()
        positions.append({
            "name": name,
            "ra": str(ra),
            "dec": str(dec),
            "distance": f"{distance.au:.3f} AU"
        })

    return positions

@app.route('/', methods=['GET', 'POST'])
def index():
    positions = []
    if request.method == 'POST':
        dob = request.form['dob']
        lat = float(request.form['latitude'])
        lon = float(request.form['longitude'])
        positions = get_planetary_positions(dob, lat, lon)
    return render_template('index.html', positions=positions)

def get_planetary_positions_api(dob_str, latitude, longitude):
    eph = load('de421.bsp')
    ts = load.timescale()
    dob = datetime.strptime(dob_str, "%Y-%m-%d %H:%M").replace(tzinfo=utc)
    t = ts.utc(dob)

    observer = Topos(latitude_degrees=latitude, longitude_degrees=longitude)
    earth = eph['earth']

    bodies = {
        'Sun': eph['sun'],
        'Moon': eph['moon'],
        'Mercury': eph['mercury'],
        'Venus': eph['venus'],
        'Mars': eph['mars'],
        'Jupiter': eph['jupiter barycenter'],
        'Saturn': eph['saturn barycenter'],
        'Uranus': eph['uranus barycenter'],
        'Neptune': eph['neptune barycenter'],
        'Pluto': eph['pluto barycenter'],
    }

    positions = []
    for name, body in bodies.items():
        astrometric = (earth + observer).at(t).observe(body).apparent()
        ra, dec, distance = astrometric.radec()
        positions.append({
            "name": name,
            "right_ascension": str(ra),
            "declination": str(dec),
            "distance_au": f"{distance.au:.3f}"
        })

    return positions

@app.route('/api/planetary-positions', methods=['POST'])
def planetary_positions():
    try:
        data = request.get_json()
        dob = data['dob']  # format: "YYYY-MM-DD HH:MM"
        lat = float(data['latitude'])
        lon = float(data['longitude'])

        positions = get_planetary_positions_api(dob, lat, lon)
        return jsonify({
            "status": "success",
            "data": positions
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
