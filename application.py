from Flask import Flask, json
import datetime as dt
import sqlalchemy
from dbsetup import session, Measurement, Station, engine

app = Flask(__name__)

@app.route('/api/v1.0/precipitation/')
def precipv1():
    weather_rows = engine.execute("""
    SELECT m.date, round(avg(m.tobs), 2) as temp
    FROM Measurement m
    WHERE strftime("%Y", m.date) = '2017'
    GROUP BY 1
    ORDER BY 1
    """).fetchall()
    vals = 'k:v for k,v in weather_rows}
    return jsonify(vals)

@app.route('/api/v1.0/stations/')
def stations_route():
    station_list = {}
    station_list['data'] = []

    for row in session.query(Station):
        station_list['data'].append(
            {"id": row.id,
            "station": row.station,
            "lat": row.latitude,
            "lng": row.longitude,
            "elev": row.elevation}
        )
    return jsonify(station_list)

@app.route('/api/v1.0/<start>/<end>')
def start_end_stations(start, end):
    weather_rows = engine.execute("""
            SELECT
                round(avg(m.tobs), 2) as avg_temp,
                round(min(m.tobs), 2) as min_temp,
                round(max(m.tobs), 2) as max_temp
                FROM Measurement m
                WHERE m.date BETWEEN '{}' AND '{}'
                ORDER BY 1
    """.format(start_date, end_date)).fetchall()
    return {"data": [dict(x) for x in weather_rows]}

app.run(debug=True)