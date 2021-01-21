#!/usr/bin/python3
# -*- coding: utf-8 -*-

import constants
from typing import Dict, List, Generator


class DataVerifier:
    def __init__(self, data: Dict[str, Dict[str, List[int]]]):
        # TODO: Check that number of groups in each cohort class matches the pre-defined respective NUM_OF_GROUPS constants
        self.status = self.check_has_exact_keys(data) and self.check_for_no_duplicates(
            data
        )

    def check_has_exact_keys(self, data: Dict[str, Dict[str, List[int]]]) -> bool:
        return list(data.keys()) == list(constants.COHORT_CLASSES.keys())

    def check_for_no_duplicates(self, data: Dict[str, Dict[str, List[int]]]) -> bool:
        temp = [
            j for cohort in [i.items() for i in list(data.values())] for _, j in cohort
        ]
        return not list(self.find_dupe(temp))

    def find_dupe(self, data: List[List[int]]) -> Generator[int, None, None]:
        seen = set()
        for lst in data:
            for item in lst:
                if item in seen:
                    yield item
                seen.add(item)
