#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Main program entry point
# Created by James Raphael Tiovalen (2020)

# Import helper scripts
import scraper.design
import scraper.dw
import processor.generate_graph
import processor.plot_graph
import utils.plot_histogram
import utils.verify_data
import sys


class MainProgramHandler:
    def __init__(self):
        # Initialize variables
        design = scraper.design.DesignTeams()
        dw = scraper.dw.DWTeams()

        # Get the corresponding teams (student ID groupings list)
        self.design_teams = design.teams
        self.dw_teams = dw.teams

        # Verify that the data is valid
        self.design_verifier = utils.verify_data.DataVerifier(self.design_teams)
        self.dw_verifier = utils.verify_data.DataVerifier(self.dw_teams)
        try:
            assert self.design_verifier.status and self.dw_verifier.status
        except AssertionError:
            print(
                "It seems that the data is invalid! Please check the data manually and ensure that the data is of the correct format and fulfill the specified requirements."
            )
            sys.exit()

    # Run graph-based algorithm to produce the required graphs
    def generate_graphs(self):
        self.final_graphs = processor.generate_graph.FinalGraphs(
            self.design_teams, self.dw_teams
        )

    # Calculate graph edit distance and convert to similarity percentage (teammate retention rate)
    def calculate_teammate_retention_rate(self):
        self.final_graphs.set_complement_graphs()
        first_estimate = (
            self.final_graphs.get_similarity_rate_compared_to_complement_graphs()
        )

        self.final_graphs.set_empty_graphs()
        second_estimate = (
            self.final_graphs.get_similarity_rate_compared_to_empty_graphs()
        )

        self.final_graphs.set_null_graph()
        control_estimate = (
            self.final_graphs.get_similarity_rate_compared_to_null_graph()
        )

        final_estimate = ((first_estimate + second_estimate) / 2) * 100

        print(
            f"Control Variable Value: {control_estimate}\n"
        )  # This should display 0.0
        print(f"Final Teammate Retention Rate: {round(final_estimate, 1)}%")

    # Plot the graphs for visualization
    def plot_graphs(self):
        self.plotter = processor.plot_graph.PlottingMethods(
            self.design_teams, self.dw_teams
        )
        self.plotter.plot_using_graphviz()

    # Plot extra count plots for appendix (for verification and further explanation purposes)
    def plot_countplots(self):
        utils.plot_histogram.plot_groups(
            self.design_teams, "DESIGN", "design_countplot.png"
        )
        utils.plot_histogram.plot_groups(self.dw_teams, "DW", "dw_countplot.png")


if __name__ == "__main__":
    handler = MainProgramHandler()
    handler.generate_graphs()
    handler.calculate_teammate_retention_rate()
    handler.plot_graphs()
    handler.plot_countplots()