from pyincore import IncoreClient, FragilityService, MappingSet
from pyincore.analyses.buildingdamage import BuildingDamage
from pyincore.globals import INCORE_API_DEV_URL


def run_with_base_class():
    client = IncoreClient(INCORE_API_DEV_URL)

    # Memphis Earthquake damage
    # New madrid earthquake using Atkinson Boore 1995
    hazard_type = "earthquake"
    hazard_id = "5b902cb273c3371e1236b36b"

    # Building dataset
    # 5a284f0bc7d30d13bc081a28  5kb
    # 5bcf2fcbf242fe047ce79dad 300kb
    # 5a284f37c7d30d13bc08219c 20mb
    bldg_dataset_id = "5a284f0bc7d30d13bc081a28"

    bldg_dmg = BuildingDamage(client)
    bldg_dmg.load_remote_input_dataset("buildings", bldg_dataset_id)

    # Earthquake mapping
    mapping_id = "5b47b350337d4a3629076f2c"
    fragility_service = FragilityService(client)
    mapping_set = MappingSet(fragility_service.get_mapping(mapping_id))
    bldg_dmg.set_input_dataset('dfr3_mapping_set', mapping_set)

    result_name = "memphis_eq_bldg_dmg_result"
    bldg_dmg.set_parameter("result_name", result_name)
    bldg_dmg.set_parameter("hazard_type", hazard_type)
    bldg_dmg.set_parameter("hazard_id", hazard_id)
    bldg_dmg.set_parameter("num_cpu", 4)

    # Run Analysis
    bldg_dmg.run_analysis()

    # TSUNAMI

    hazard_type = "tsunami"
    hazard_id = "5bc9e25ef7b08533c7e610dc"

    # Seaside building dataset
    bldg_dataset_id = "5bcf2fcbf242fe047ce79dad"

    # Run seaside tsunami building damage
    bldg_dmg = BuildingDamage(client)
    bldg_dmg.load_remote_input_dataset("buildings", bldg_dataset_id)

    # Tsunami mapping
    mapping_id = "5b48fb1f337d4a478e7bd54d"
    fragility_service = FragilityService(client)
    mapping_set = MappingSet(fragility_service.get_mapping(mapping_id))
    bldg_dmg.set_input_dataset('dfr3_mapping_set', mapping_set)

    result_name = "seaside_tsunami_dmg_result"
    bldg_dmg.set_parameter("result_name", result_name)
    bldg_dmg.set_parameter("hazard_type", hazard_type)
    bldg_dmg.set_parameter("hazard_id", hazard_id)
    bldg_dmg.set_parameter("num_cpu", 4)
    bldg_dmg.run_analysis()


if __name__ == '__main__':
    run_with_base_class()
