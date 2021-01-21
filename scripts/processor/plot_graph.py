#!/usr/bin/python3
# -*- coding: utf-8 -*-

from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import networkx as nx
import pygraphviz as pgv
import matplotlib.pyplot as plt
from typing import Dict, List


class PlottingMethods:
    def __init__(
        self,
        design_teams: Dict[str, Dict[str, List[int]]],
        dw_teams: Dict[str, Dict[str, List[int]]],
    ):
        all_design_groupings = []
        all_dw_groupings = []

        for class_number, values in design_teams.items():
            for team_number, team_members in values.items():
                temp = nx.complete_graph(
                    team_members
                )  # Each team is considered to be a complete subgraph
                all_design_groupings.append(temp)

        for class_number, values in dw_teams.items():
            for team_number, team_members in values.items():
                temp = nx.complete_graph(
                    team_members
                )  # Each team is considered to be a complete subgraph
                all_dw_groupings.append(temp)

        # We can do a union all since no person is in 2 different groups for the same course
        self.design_graph = nx.union_all(all_design_groupings)
        self.dw_graph = nx.union_all(all_dw_groupings)

    def plot_using_matplotlib(self):
        # Plot 03.007's graph and save it to a file
        nx.draw_networkx(self.design_graph, arrows=False, with_labels=False)
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.savefig("design_graph.png")

        # Prepare canvas by clearing the current figure
        plt.clf()

        # Plot 10.009's graph and save it to a file
        nx.draw_networkx(self.dw_graph, arrows=False, with_labels=False)
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.savefig("dw_graph.png")

    def plot_using_graphviz(self):
        # Add label property to all nodes in the two graphs (so as to hide all the actual student IDs)
        for node in self.design_graph.nodes():
            self.design_graph.nodes[node]["label"] = ""

        for node in self.dw_graph.nodes():
            self.dw_graph.nodes[node]["label"] = ""

        # Create Graphviz-based AGraph objects for the two courses
        design_agraph_plot = nx.nx_agraph.to_agraph(self.design_graph)
        dw_agraph_plot = nx.nx_agraph.to_agraph(self.dw_graph)

        # Add positions to the nodes using the default `neato` Graphviz layout algorithm
        design_agraph_plot.layout()
        dw_agraph_plot.layout()

        # Render the graphs to image files
        design_agraph_plot.draw("design_graph.png")
        dw_agraph_plot.draw("dw_graph.png")