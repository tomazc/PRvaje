from geopy import geocoders
g = geocoders.GoogleV3()
place, (lat, lng) = g.geocode("%s %s" % ("Bovec", "Slovenija"), exactly_one=False)[0]
print place, lat, lng
