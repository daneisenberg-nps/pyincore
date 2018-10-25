import math
import csv
import collections


class NonStructBuildingUtil:
    BUILDING_FRAGILITY_KEYSBUILDING_FRAGILITY_KEYS = {
        "drift-sensitive fragility id code": ["Drift Sensitive", "DS"],
        "parametric non-retrofit fragility id code": ["Parametric Non-Retrofit", "PNR"],
        "acceleration-sensitive fragility id code": ["Acceleration Sensitive", "AS"],
        "non-retrofit fragility id code": ["as built", "none"]
    }

    DEFAULT_FRAGILITY_KEY_DS = "Drift-Sensitive Fragility ID Code"
    DEFAULT_FRAGILITY_KEY_AS = "Acceleration-Sensitive Fragility ID Code"

    @staticmethod
    def get_damage_ratio_rows(csv_reader: csv.DictReader):
        csv_rows = []

        # Ignore the header
        row_index = 0
        for row in csv_reader:
            if row_index > 0:
                csv_rows.append(row)

            row_index += 1

        return csv_rows

    @staticmethod
    def get_damage_ratio_values(rows, column: str):
        dmg_ratio_values = []
        for row in rows:
            dmg_ratio_values.append(row[column])

        return dmg_ratio_values

    @staticmethod
    def get_dmg_weights(dmg_ratio_tbl):
        dmg_weights = [float(row['Mean Damage Factor']) for row in
                       dmg_ratio_tbl]

        return dmg_weights

    @staticmethod
    def get_dmg_weights_std_dev(dmg_ratio_tbl):
        dmg_weights_std_dev = [float(row['Deviation Damage Factor']) for
                               row in dmg_ratio_tbl]

        return dmg_weights_std_dev

    @staticmethod
    def get_building_period(num_stories, fragility_set):
        period = 0.0

        fragility_curve = fragility_set['fragilityCurves'][0]
        if fragility_curve[
            'className'] == 'edu.illinois.ncsa.incore.services.fragility.model.PeriodStandardFragilityCurve':
            period_equation_type = fragility_curve['periodEqnType']
            if period_equation_type == 1:
                period = fragility_curve['periodParam0']
            elif period_equation_type == 3:
                period = fragility_curve['periodParam0'] * num_stories
            elif period_equation_type == 3:
                period = fragility_curve['periodParam1'] * math.pow(
                    fragility_curve['periodParam0'] * num_stories,
                    fragility_curve['periodParam2'])

        return period

    @staticmethod
    def get_hazard_demand_type(building, fragility_set, hazard_type):
        fragility_hazard_type = fragility_set['demandType'].lower()
        hazard_demand_type = fragility_hazard_type

        if hazard_type.lower() == "earthquake":
            num_stories = building['properties']['no_stories']
            building_period = NonStructBuildingUtil.get_building_period(num_stories,
                                                               fragility_set)

            if fragility_hazard_type.endswith(
                    'sa') and fragility_hazard_type != 'sa':
                # This fixes a bug where demand type is in a format similar to 1.0 Sec Sa
                if len(fragility_hazard_type.split()) > 2:
                    building_period = fragility_hazard_type.split()[0]
                    fragility_hazard_type = "Sa"

            hazard_demand_type = fragility_hazard_type

            # This handles the case where some fragilities only specify Sa, others a specific period of Sa
            if not hazard_demand_type.endswith('pga'):
                hazard_demand_type = str(
                    building_period) + " " + fragility_hazard_type

        return hazard_demand_type

    @staticmethod
    def adjust_damage_for_liquefaction(limit_state_probabilities, ground_failure_probabilities):
        """
        Adjusts building damage probability based on liquefaction ground failure probability
        with the liq_dmg, we know that it is 3 values, the first two are the
		same. The 3rd might be different.
		we always want to apply the first two to all damage states except the highest.
        Args:
            limit_state_probabilities:
            ground_failure_probabilities:

        Returns: adjusted limit state probability

        """
        keys = list(limit_state_probabilities.keys())
        adjusted_limit_state_probabilities = collections.OrderedDict()

        for i in range(len(keys)):
            # check and see...if we are trying to use the last ground failure
            # number for something other than the
            # last limit-state-probability, then we should use the
            # second-to-last probability of ground failure instead.

            if i > len(ground_failure_probabilities) -1:
                prob_ground_failure = ground_failure_probabilities[len(ground_failure_probabilities)-2]
            else:
                prob_ground_failure = ground_failure_probabilities[i]

            adjusted_limit_state_probabilities[keys[i]] = limit_state_probabilities[keys[i]] + prob_ground_failure \
                                                - limit_state_probabilities[keys[i]] * prob_ground_failure

        # the final one is the last of limitStates should match with the last
		# of ground failures
        j = len(limit_state_probabilities) - 1
        prob_ground_failure = ground_failure_probabilities[-1]
        adjusted_limit_state_probabilities[keys[j]] = limit_state_probabilities[keys[j]] + prob_ground_failure \
                                            - limit_state_probabilities[keys[j]] * prob_ground_failure

        return adjusted_limit_state_probabilities


