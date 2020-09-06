from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import argparse

NAMESPACE = "{http://www.topografix.com/GPX/1/1}"
TIMESTAMP_FORMAT = "%Y/%m/%d %H:%M"

if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description="GaiaGPS Stravafier")
    required_parser = argParser.add_argument_group("required arguments")
    required_parser.add_argument('-file', help="The GPX file you're converting", required=True)
    required_parser.add_argument('-start', help="Activity start timestamp (ie. '2020/09/05 9:30')", required=True)
    required_parser.add_argument('-end', help="Activity end timestamp (ie. '2020/09/05 13:30')", required=True)
    args = argParser.parse_args()

    print("----------------------------------------------------")
    print("Converting GaiaGPS GPX file to Stava-friendly GPX...")
    print("----------------------------------------------------")

    inputXML = ET.parse(args.file).getroot()
    startDate = datetime.strptime(args.start, TIMESTAMP_FORMAT)
    endDate = datetime.strptime(args.end, TIMESTAMP_FORMAT)

    # Start building our new GPX file
    gpx = ET.Element('gpx')
    gpx.set('creator', 'GaiaGPS')
    gpx.set('version', '1.1')
    gpx.set('xmlns', 'http://www.topografix.com/GPX/1/1')
    gpx.set('xmlns:gpxtpx', 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1')
    gpx.set('xmlns:gpxx', 'http://www.garmin.com/xmlschemas/GpxExtensions/v3')
    gpx.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    gpx.set('xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd')
    trk = ET.SubElement(gpx, 'trk')
    name = ET.SubElement(trk, 'name')
    name.text = inputXML[0][0].text
    activityType = ET.SubElement(trk, 'type')
    trkseg = ET.SubElement(trk, 'trkseg')

    # Calculate an average number of seconds per segment
    # Then use that to generate approximate times for each segment (required by Strava)
    durationSeconds = endDate.timestamp() - startDate.timestamp()
    segmentCount = len(inputXML[0].getchildren())
    secondsPerSegment = durationSeconds/segmentCount
    runningTime = startDate.timestamp()

    print(" - Incoming file: " + args.file)
    print(" - Activity: " + name.text)
    print(" - Start: " + startDate.strftime(TIMESTAMP_FORMAT))
    print(" - End: " + endDate.strftime(TIMESTAMP_FORMAT))
    print(" - Ellapsed: " + str(durationSeconds) + " seconds")
    print(" - Segments: " + str(segmentCount))
    print(" - Average: " + str(secondsPerSegment) + " sec/segment")

    # For each segment in the old file, create one in the new file
    for rtept in inputXML.iter(NAMESPACE + 'rtept'):

        trkpt = ET.SubElement(trkseg, 'trkpt')
        trkpt.set('lat', rtept.get('lat'))
        trkpt.set('lon', rtept.get('lon'))
        ele = ET.SubElement(trkpt, 'ele')
        ele.text = rtept.find(NAMESPACE + 'ele').text

        time = ET.SubElement(trkpt, 'time')
        time.text = str(datetime.fromtimestamp(runningTime).astimezone().isoformat())
        runningTime += secondsPerSegment

    # Write our new-and-improved, Strava-friendly GPX file
    with open("data/gaiagps-converted.gpx", "w") as output:
        output.write(ET.tostring(gpx).decode("utf-8"))

    print("Conversion complete! [See: data/gaiagps-converted.gpx]")
