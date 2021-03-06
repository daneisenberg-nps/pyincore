# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/

from pyincore import IncoreClient
from pyincore.analyses.populationdislocation import PopulationDislocation, PopulationDislocationUtil


def run_with_base_class():
    client = IncoreClient()

    # Joplin
    # kube-dev
    building_dmg = "5df815ec425e0b00092daee1"
    housing_unit_alloc = "5df7c989425e0b00092c5eb4"
    bg_data = "5df7cb0b425e0b00092c9464"
    value_loss = "5df8384a425e0b00092de799"

    pop_dis = PopulationDislocation(client)

    pop_dis.load_remote_input_dataset("building_dmg", building_dmg)
    pop_dis.load_remote_input_dataset("housing_unit_allocation", housing_unit_alloc)
    pop_dis.load_remote_input_dataset("block_group_data", bg_data)
    pop_dis.load_remote_input_dataset("value_poss_param", value_loss)

    # pop_dis.show_gdocstr_docs()

    result_name = "pop-dislocation-results"
    seed = 1111

    pop_dis.set_parameter("result_name", result_name)
    pop_dis.set_parameter("seed", seed)

    pop_dis.run_analysis()


if __name__ == '__main__':
    run_with_base_class()
