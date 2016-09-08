# This script makes a spreadsheet from NOAA hurricane advisories.

import forecast_parser as fp

ADVISORY_ARCHIVE_URL = "" # The web address of the NOAA advisory archive for
                          #your hurricane
OUTPUT_SPREADSHEET_FILE = "" # the file path the spreadsheet will be saved at

# first, create a list to store our results
advisory_information_list = list()

# This function returns a list with the web addresses of each hurricane advisory
advisory_url_list = fp.get_advisory_urls(ADVISORY_ARCHIVE_URL)
print "found %s advisories" % len(advisory_url_list)
# now we construct a loop
for url in advisory_url_list:
    # for each url in the list, the following steps will be preformed
    # this function gets the hurricane information from the advisory webpage
    advisory_information = fp.get_advisory_dictionary(url)
    # this function adds that information to our list
    advisory_information_list.append(advisory_information)

# this function makes a spreadsheet from the list
fp.advisory_list_to_csv(advisory_information_list, OUTPUT_SPREADSHEET_FILE)
