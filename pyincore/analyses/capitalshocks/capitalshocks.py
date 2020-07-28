from pyincore import BaseAnalysis
import pandas as pd
import numpy as np


class CapitalShocks(BaseAnalysis):
    """Capital stock shocks for an individual building is equal to the functionality probability multiplied by value
     of the building. This gives us the capital stock loss in the immediate aftermath of a natural disaster
     for a single building. We aggregate each of these individual losses to their associated economic sector
     to calculate the total capital stock lost for that sector. However, the capital stock shocks that are
     used as inputs into the CGE model are scalars for embodying the percent of capital stock remaining.
     We get this by dividing the total capital stock remaining by the total capital stock
     before the natural disaster."

    Args:
        incore_client (IncoreClient): Service authentication.

    """

    def __init__(self, incore_client):
        super(CapitalShocks, self).__init__(incore_client)

    def get_spec(self):
        return {
            'name': 'Capital Shocks',
            'description': 'Capital Shocks generation for Joplin cge model.',
            'input_parameters': [],
            'input_datasets': [
                {
                    'id': 'buildings',
                    'required': True,
                    'description': 'Building Inventory',
                    'type': ['ergo:buildingInventoryVer5', 'ergo:buildingInventoryVer6'],
                },
                {
                    'id': 'buildings_to_sectors',
                    'required': True,
                    'description': 'Failure probability of buildings.',
                    'type': ['incore:buildingsToSectors']
                },
                {
                    'id': 'failure_probability',
                    'required': True,
                    'description': 'Failure probability of buildings.',
                    'type': ['incore:failureProbability']
                }
            ],
            'output_datasets': [
                {
                    'id': 'sector_shocks',
                    'required': True,
                    'description': 'Aggregation of building functionality states to capital shocks per sector',
                    'type': ['incore:CapitalShocks']
                }
            ]
        }

    def run(self):
        buildings = self.get_input_dataset("buildings").get_inventory_reader()
        buildings_df = pd.DataFrame(list(buildings))
        failure_probability = \
            pd.read_csv(self.get_input_dataset("failure_probability").get_file_path('csv'), index_col=0)
        buildings_to_sectors = \
            pd.read_csv(self.get_input_dataset("buildings_to_sectors").get_file_path('csv'), index_col=0)

        # drop buildings with no sector
        buildings_to_sectors = buildings_to_sectors[pd.notnull(buildings_to_sectors['sector'])]
        building_inventory = pd.DataFrame.from_records(buildings_df["properties"])
        # drop buildings with no appraisal value
        building_inventory = building_inventory[pd.notnull(building_inventory['appr_bldg'])]
        building_inventory['appr_bldg'] = building_inventory['appr_bldg'].astype(float)
        # drop buildings with no failure probability
        failure_probability = failure_probability[pd.notnull(failure_probability['failure_probability'])]

        inventory_failure = pd.merge(building_inventory, failure_probability, on='guid')
        inventory_failure = pd.merge(inventory_failure, buildings_to_sectors, on='guid')
        inventory_failure['cap_rem'] = inventory_failure.appr_bldg * (
                    1 - inventory_failure.failure_probability)

        sectors = buildings_to_sectors.sector.unique()
        sector_shocks = {}
        for sector in sectors:
            sector_values = inventory_failure.loc[(inventory_failure['sector'] == sector)]
            sector_cap = sector_values['cap_rem'].sum()
            sector_total = sector_values['appr_bldg'].sum()
            if sector_total == 0:
                continue
            sector_shock = np.divide(sector_cap, sector_total)
            sector_shocks[sector] = sector_shock

        sector_shocks = pd.DataFrame(sector_shocks.items(), columns=['sector', 'shock'])
        self.set_result_csv_data("sector_shocks", sector_shocks, name="sector_shocks.csv", source="dataframe")

        return True