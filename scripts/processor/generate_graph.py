#!/usr/bin/python3
# -*- coding: utf-8 -*-

import networkx as nx
import gmatch4py as gm
import numpy as np
from typing import Dict, List


class FinalGraphs:
    """
    Class of helper functions to build the final overall 2 graphs
    """

    def __init__(
        self,
        design_teams: Dict[str, Dict[str, List[int]]],
        dw_teams: Dict[str, Dict[str, List[int]]],
    ):
        all_design_groupings = []
        all_dw_groupings = []
        self.ged = gm.GraphEditDistance(
            1, 1, 1, 1
        )  # All edit costs are equal to 1 (these are modification costs, which are not weights of the graphs' edges to be very precise)

        for class_number, values in design_teams.items():
            for team_number, team_members in values.items():
                temp = nx.complete_graph(
                    team_members
                )  # Each team is considered to be a complete subgraph (clique)
                all_design_groupings.append(temp)

        for class_number, values in dw_teams.items():
            for team_number, team_members in values.items():
                temp = nx.complete_graph(
                    team_members
                )  # Each team is considered to be a complete subgraph (clique)
                all_dw_groupings.append(temp)

        # We can do a union all since no person is in 2 different groups for the same course
        self.design_graph = nx.union_all(all_design_groupings)
        self.dw_graph = nx.union_all(all_dw_groupings)

        # We only need to compare the 03.007 groupings and the 10.009 groupings to each other once, even as we utilize different benchmarks/thresholds in the subsequent functions/methods (order matters for non-symmetrical cost matrices and their corresponding "meanings")
        self.design_dw_result = self.ged.compare(
            [self.design_graph, self.dw_graph], None
        )

    def set_complement_graphs(self):
        self.complement_design_graph = nx.algorithms.operators.unary.complement(
            self.design_graph
        )
        self.complement_dw_graph = nx.algorithms.operators.unary.complement(
            self.dw_graph
        )

    def get_similarity_rate_compared_to_complement_graphs(self) -> np.float64:
        design_complement_result = self.ged.compare(
            [self.design_graph, self.complement_design_graph], None
        )
        dw_complement_result = self.ged.compare(
            [self.dw_graph, self.complement_dw_graph], None
        )

        design_side_similarity_percentage = (
            self.design_dw_result[1, 0] / design_complement_result[1, 0]
        )
        dw_side_similarity_percentage = (
            self.design_dw_result[0, 1] / dw_complement_result[1, 0]
        )

        # Use and return the average as a very, very, very rough method (since the 03.007 graph contains slightly different vertices in overall compared to the 10.009 graph)
        return (design_side_similarity_percentage + dw_side_similarity_percentage) / 2

    def set_empty_graphs(self):
        self.empty_design_graph = nx.create_empty_copy(self.design_graph)
        self.empty_dw_graph = nx.create_empty_copy(self.dw_graph)

    def get_similarity_rate_compared_to_empty_graphs(self) -> np.float64:
        design_empty_result = self.ged.compare(
            [self.design_graph, self.empty_design_graph], None
        )
        dw_empty_result = self.ged.compare([self.dw_graph, self.empty_dw_graph], None)

        design_side_similarity_percentage = (
            self.design_dw_result[1, 0] / design_empty_result[1, 0]
        )
        dw_side_similarity_percentage = (
            self.design_dw_result[0, 1] / dw_empty_result[1, 0]
        )

        # Use and return the average as a very, very, very rough method (since the 03.007 graph contains slightly different vertices in overall compared to the 10.009 graph)
        return (design_side_similarity_percentage + dw_side_similarity_percentage) / 2

    def set_null_graph(self):
        self.null_graph = nx.empty_graph(0)

    # Use this as control variable (should return 0.0 since values are divided by infinity)
    def get_similarity_rate_compared_to_null_graph(self) -> np.float64:
        design_null_result = self.ged.compare(
            [self.design_graph, self.null_graph], None
        )
        dw_null_result = self.ged.compare([self.dw_graph, self.null_graph], None)

        design_side_similarity_percentage = (
            self.design_dw_result[1, 0] / design_null_result[1, 0]
        )
        dw_side_similarity_percentage = (
            self.design_dw_result[0, 1] / dw_null_result[1, 0]
        )

        # Use and return the average as a very, very, very rough method (since the 03.007 graph contains slightly different vertices in overall compared to the 10.009 graph)
        return (design_side_similarity_percentage + dw_side_similarity_percentage) / 2