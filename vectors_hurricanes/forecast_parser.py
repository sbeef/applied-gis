from bs4 import BeautifulSoup
import urllib2
import re
import csv

BASE_URL = 'http://www.nhc.noaa.gov'

TIME_AND_POS_REGEX = '[\s\S]*(\d\d\d\d) UTC \w\w\w (\w\w\w \d\d \d\d\d\d)[\s\S]*CENTER LOCATED NEAR ([\d.]+)N\s*([\d.]+)W.*\nPOSITION ACCURATE WITHIN\s+(\d+)\s*NM'
CURRENT_WINDS_REGEX = '[\s\S]*MAX SUSTAINED WINDS.*\n([\s\S]*)\nWINDS[\s\S]*'
SPEEDS_REGEX = '.*KT[^\d]*(\d+)(\w+)\s*(\d+)(\w+)\s*(\d+)(\w+)\s*(\d+)(\w+)'
FORECAST_REGEX = '(FORECAST VALID.*W.*\nMAX WIND.*KT.\n(.*NW.\n)*)' 
FORECAST_POSITION_REGEX = 'FORECAST VALID.*Z\s([\d.]+)N\s*([\d.]+)W'
FORECAST_WINDS_REGEX = '\n(\d\d KT[\s\S]*NW.)'

CSV_HEADER = ['number', 'date', 'time', 'elapsed_time', 'latitude', 'longitude',
              'error', 'HFW', 'TSFW', '12hr_lat', '12hr_long', '12hr_hfw', 
              '12hr_tsfw', '24hr_lat', '24hr_long', '24hr_hfw', '24hr_tsfw',
              '36hr_lat', '36hr_long', '36hr_hfw', '36hr_tsfw']

HFW_VALUE = 64
TSFW_VALUE = 50

def get_advisory_time_and_position(advisory_string, results):
    t = re.compile(TIME_AND_POS_REGEX)
    match = t.match(advisory_string)
    results['time'] = match.group(1)
    results['date'] = match.group(2)
    results['latitude'] = match.group(3)
    results['longitude'] = match.group(4)
    results['error'] = match.group(5)
    return results

def get_wind(winds_string, speed):
    winds = winds_string.split('\n')
    for wind in winds:
        if wind[:2] == str(speed):
            return wind
    return None

def get_radii(wind_string):
    if wind_string == None:
        return None
    p = re.compile(SPEEDS_REGEX)
    print type(wind_string)
    match = p.match(wind_string)
    results = {} 
    for i in range(0, len(match.groups()), 2):
        results[match.groups()[i+1]] = int(match.groups()[i])
    return results

def get_mean_radius(radii):
    if radii == None:
        return None
    return sum(radii.values())/float(len(radii.values()))

def get_hfw(winds_string):
    return get_radii(get_wind(winds_string, HFW_VALUE))

def get_tsfw(winds_string):
    return get_radii(get_wind(winds_string, TSFW_VALUE))

def get_current_winds(advisory_string, results):
    w = re.compile(CURRENT_WINDS_REGEX)
    match = w.match(advisory_string)
    winds = match.group(1)
    hfw = get_hfw(winds)
    tsfw = get_tsfw(winds)
    results['HFW'] = get_mean_radius(hfw)
    results['TSFW'] = get_mean_radius(tsfw)
    return results
   
def get_forecast_location(forecast_string):
    f = re.compile(FORECAST_POSITION_REGEX)
    position = f.match(forecast_string)
    return [float(dec) for dec in position.groups()]

def get_forecast_winds(forecast_string):
    w = re.compile(FORECAST_WINDS_REGEX)
    match = w.search(forecast_string)
    return match.group(1)

def get_forecast_information(forecast_string, name, results):
    location = get_forecast_location(forecast_string)
    winds = get_forecast_winds(forecast_string)
    hfw = get_hfw(winds)
    tsfw = get_tsfw(winds)
    results["%s_lat" % name] = location[0]
    results["%s_long" % name] = location[1]
    results["%s_hfw" % name] = get_mean_radius(hfw)
    results["%s_tsfw" % name] = get_mean_radius(tsfw)
    return results


def get_forecasts(advisory_string, results):
    f = re.compile(FORECAST_REGEX)
    forecasts = f.findall(advisory_string)
    results = get_forecast_information(forecasts[0][0], '12hr', results)
    results = get_forecast_information(forecasts[1][0], '24hr', results)
    results = get_forecast_information(forecasts[2][0], '36hr', results)
    return results
    
def get_advisories(archive_soup):
    days = archive_soup.find_all(headers='col1')
    advisory_urls = []
    for day in days:
        for link in day.find_all('a'):
            href = link.get('href')
            full_link = "%s%s" % (BASE_URL, href)
            advisory_urls.append(full_link)
    return advisory_urls

def get_old_advisories(archive_soup):
    table_rows = archive_soup.find_all('tr')
    column_one = [row.find('td') for row in table_rows]
    advisory_urls = []
    for entry in column_one:
        if entry is not None:
            for link in entry.find_all('a'):
                href = link.get('href')
                full_link = "%s%s" % (BASE_URL, href)
                advisory_urls.append(full_link)
    return advisory_urls

def is_old_advisory(archive_soup):
    if len(archive_soup.find_all('meta')) == 3:
        return True
    else:
        return False

def get_advisory_urls(archive_url):
    archive_string = urllib2.urlopen(archive_url).read()
    archive_soup = BeautifulSoup(archive_string, 'html.parser')
    if is_old_advisory(archive_soup):
        return get_old_advisories(archive_soup)
    else:
        return get_advisories(archive_soup)

def get_advisory_dict(advisory_url, results):
    advisory_string = urllib2.urlopen(advisory_url).read()
    results = get_advisory_time_and_position(advisory_string, results)
    results = get_current_winds(advisory_string, results)
    results = get_forecasts(advisory_string, results)
    return results

def get_advisory_dictionary(url):
    number = int(url[-8:-5])
    return get_advisory_dict(url, {'number': number})

def advisory_list_to_csv(advisory_list, output_file):
    csv_file = open(output_file, 'w')
    writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADER)
    writer.writeheader()
    for advisory in advisory_list:
        writer.writerow(advisory)
    csv_file.close()


def get_advisories_list(archive_url):
    advisory_urls = get_advisory_urls(archive_url)
    advisories_list = []
    for index, url in enumerate(advisory_urls):
        advisories_list.append(get_advisory_dict(url, {'number': index+1}))
    return advisories_list
