#!/usr/bin/python3
# -*- coding: utf-8 -*-

import constants
import gspread
import re


class DWTeams:
    """
    Class of helper functions to scrape 10.009 The Digital World groups.
    """

    def __init__(self):
        self.key = constants.GOOGLE_SHEETS_DW_KEY
        self.teams = (
            {}
        )  # This attribute is used to store the final overall 10.009 groupings dictionary
        self.gc = gspread.service_account()
        self.sh = self.gc.open_by_key(self.key)
        self.cohort_classes = self.sh.worksheets()[0:8]
        self.get_all_dw_groups()

    def get_single_class_dw_groups(self, cohort_class_code):
        class_index = constants.COHORT_CLASSES.get(cohort_class_code)
        worksheet = self.cohort_classes[class_index]
        values = worksheet.get_all_values()
        class_grouping = {}
        index = 2  # Skip the first two unimportant rows

        while index < len(values):
            counter = 1

            if bool(
                re.search("^Team\s[1-8]-(10|[1-9])$", values[index][0].strip())
            ):  # Use regex to check if row entry starts with valid team number (this will skip the invalid hidden extra team numbers at the end of each worksheet)
                current_grouping = []

                for row in values[
                    index + 2 : index + 8
                ]:  # Skip the header row and max number of team members is 6
                    if bool(
                        re.search("^100[0-9]{4}$", row[3].strip())
                    ):  # Check if student ID is present
                        current_grouping.append(int(row[3].strip()))
                        counter += 1  # Increase counter

                    else:
                        break  # Break the loop so as to not over-add the counter since processing for current team is finished

                class_grouping[
                    values[index][0]
                ] = current_grouping  # Add current team's grouping list to overall class grouping dictionary

            index += counter  # Skip the already-processed rows to be more efficient

        return class_grouping

    def get_all_dw_groups(self):
        for class_code in list(constants.COHORT_CLASSES.keys()):
            self.teams[class_code] = self.get_single_class_dw_groups(class_code)