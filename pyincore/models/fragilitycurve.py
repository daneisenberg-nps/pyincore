# Copyright (c) 2019 University of Illinois and others. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/


class FragilityCurve:
    """
    abstract class for fragility curves.
    """

    def __init__(self, curve_parameters):
        self.description = curve_parameters['description']

    def calculate_limit_state_probability(self, hazard, period: float = 0.0, std_dev: float = 0.0, **kwargs):
        """
            Computes limit state probabilities.
            Args:
                hazard: hazard value to compute probability for
                period: building period default to 0
                std_dev: standard deviation

            Returns: limit state probability

        """
        probability = float(0.0)
        return probability

    def adjust_fragility_for_liquefaction(self, liquefaction: str):
        """Adjusts fragility curve object by input parameter liquefaction.

        Args:
            liquefaction (str): Liquefaction type.

        Returns:
        """
        raise NotImplementedError("This function is currently only applied to Standard Fragility Curve, "
                                  "and Period Standard Fragility Curve")

    def get_building_period(self, num_stories):
        """Get building period from the fragility curve.

        Args:
            num_stories (int): Number of building stories.

        Returns:
            float: Building period.

        """
        period = 0.0
        return period

    def compute_custom_limit_state_probability(self, variables: dict):
        """Computes custom limit state probabilities.
            Args:
                variables: variables to set

            Returns: limit state probability
        """
        probability = float(0.0)
        return probability
