from datetime import datetime, timezone
import xml.etree.ElementTree as ET

NAMESPACE = "{http://www.topografix.com/GPX/1/1}"

if __name__ == "__main__":

    print("Converting GaiaGPS GPX file to Stava-friendly GPX...")

    inputXML = ET.parse('triple-climb-garland-ranch.gpx').getroot()

    # Set up our outputXML
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

    #datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)
    startDate = datetime(2020, 9, 5, 6, 30, 0, 0)
    endDate = datetime(2020, 9, 5, 11, 10, 0, 0)

    durationSeconds = endDate.timestamp() - startDate.timestamp()
    segmentCount = len(inputXML[0].getchildren())
    secondsPerSegment = durationSeconds/segmentCount
    runningTime = startDate.timestamp()

    for rtept in inputXML.iter(NAMESPACE + 'rtept'):

        trkpt = ET.SubElement(trkseg, 'trkpt')
        trkpt.set('lat', rtept.get('lat'))
        trkpt.set('lon', rtept.get('lon'))
        ele = ET.SubElement(trkpt, 'ele')
        ele.text = rtept.find(NAMESPACE + 'ele').text

        time = ET.SubElement(trkpt, 'time')
        time.text = str(datetime.fromtimestamp(runningTime).astimezone().isoformat())
        runningTime += secondsPerSegment


    #2020-09-05T13:49:50Z
    #2020-09-04 23:31:26.626140

    #print(ET.tostring(gpx))

    with open("gaiagps-converted.gpx", "w") as output:
        output.write(ET.tostring(gpx).decode("utf-8"))

    print("Finished!")