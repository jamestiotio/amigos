#!/usr/bin/python3
# -*- coding: utf-8 -*-

import constants


class DataVerifier:
    def __init__(self, data):
        # TODO: Check that number of groups in each cohort class matches the pre-defined respective NUM_OF_GROUPS constants
        self.status = self.check_has_exact_keys(data) and self.check_for_duplicates(
            data
        )

    def check_has_exact_keys(self, data):
        return list(data.keys()) == list(constants.COHORT_CLASSES.keys())

    def check_for_duplicates(self, data):
        temp = [
            j for cohort in [i.items() for i in list(data.values())] for _, j in cohort
        ]
        return not list(find_dupe(temp))

    def find_dupe(self, data):
        seen = set()
        for lst in data:
            for item in lst:
                if item in seen:
                    yield item
                seen.add(item)
