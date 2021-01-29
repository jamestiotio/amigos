#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Define hard-coded constants

EDIMENSION_GENERAL_URL = "edimension.sutd.edu.sg"
EDIMENSION_LOGIN_URL = "saturn.sutd.edu.sg"

# This constant is used by an extremely hacky method to detect a 503 error when loading the page (this is due to the fact that it is not possible to use the Selenium WebDriver API to get the HTTP Response Code, as per discussed ad nauseam here: https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/141)
EDIMENSION_ERROR_PAGE_SOURCE = '<html><head><title>Service Unavailable</title>\n<meta http-equiv="Content-Type" content="text/html; charset=us-ascii"></head>\n<body><h2>Service Unavailable</h2>\n<hr><p>HTTP Error 503. The service is unavailable.</p>\n\n</body></html>'

EDIMENSION_USERNAME = ""  # SUTDSTU\\100xxxx
EDIMENSION_PASSWORD = ""
# The photo roster URL anatomy includes the HTTPS protocol tag, eDimension's subdomain, the `webapps` category, the specific photo roster ID, as well as the course ID (as the query string under the `apps/roster` subcategory)
EDIMENSION_PHOTO_ROSTER_URL = ""

# This is the "public on the web" key, not the "published to the web" key
GOOGLE_SHEETS_DW_KEY = ""

# These constants define the number of groups for each class from F01/SC01 to F08/SC08 for each respective course/module
DESIGN_NUM_OF_GROUPS = [9, 10, 10, 10, 10, 10, 9, 9]
DW_NUM_OF_GROUPS = [10, 10, 10, 10, 10, 10, 10, 10]

COHORT_CLASSES = {
    "SC01": 0,
    "SC02": 1,
    "SC03": 2,
    "SC04": 3,
    "SC05": 4,
    "SC06": 5,
    "SC07": 6,
    "SC08": 7,
}
