# Gaia GPS Stravafier

A little script to convert the GPX files exported from GaiaGPS to a Strava-friendly format.

### Background

- I don't like wearing fitness trackers, but I do like tracking my activity on [Strava](https://www.strava.com/).
- I use [Gaia GPS](https://www.gaiagps.com/) for planning routes. 
- Gaia GPS will export a route as GPX file, and Strava will import GPX files, but the files from Gaia GPS aren't compatible with Strava.

### Usage

- Plan your route in Gaia GPS and go hike (or run, if you're into that). 
- Don't wear a fitness tracker, but keep track of your start and end times.
- When you get home, export the route as a GPX file from Gaia GPS, then run this script with your start and end times to generate a new GPX file.
- Upload that new file to Strava.

### Notes

All GPX files imported by Strava require each segment to include a `<time>`. The script adds approximated times by dividing the duration of your activity by the number of segments.
