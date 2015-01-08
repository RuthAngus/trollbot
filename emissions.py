import urllib2
import sys

def request(airport1, airport2):
    url = 'https://airport.api.aero/airport/distance/' +airport1 +'/' + airport2 + '?user_key=73822f31b1d54850e3483a6da29b63fc'

    req = urllib2.Request(url, None)

    response = urllib2.urlopen(req)
    the_page = response.read()

    if the_page.split('"')[10] == ':null,':

        diststr = the_page.split('"')[13]
        distfloat = float(diststr.replace(',',''))
        return distfloat

    else:
        print 'API error, unable to calculate distance'
        return 0




def distance_to_co2(km):
    if km < 3500:
        kgco2 = 1.36307304e-08*km**2  - 7.06618762e-05*km + 1.52332253e-01

    else:
        kgco2 =  1.63625000e-10*km**2 - 1.81805000e-06*km + 6.87451000e-02

    
    totco2 = kgco2 * km

    return totco2



def airports_to_co2(airport1, airport2):
    
    distance = request(airport1, airport2)


    co2 = distance_to_co2(distance)

    return co2


co2 = airports_to_co2(sys.argv[1], sys.argv[2])

print co2
