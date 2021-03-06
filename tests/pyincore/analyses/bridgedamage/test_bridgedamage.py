from pyincore import IncoreClient, FragilityService, MappingSet
from pyincore.analyses.bridgedamage import BridgeDamage
from pyincore.globals import INCORE_API_DEV_URL


def run_with_base_class():
    client = IncoreClient(INCORE_API_DEV_URL)

    # New madrid earthquake using Atkinson Boore 1995
    hazard_type = "earthquake"
    hazard_id = "5b902cb273c3371e1236b36b"

    # NBSR bridges
    bridge_dataset_id = "5a284f2dc7d30d13bc082040"

    # Default Bridge Fragility Mapping on incore-service
    mapping_id = "5b47bcce337d4a37755e0cb2"

    # Use hazard uncertainty for computing damage
    use_hazard_uncertainty = False
    # Use liquefaction (LIQ) column of bridges to modify fragility curve
    use_liquefaction = False

    # Create bridge damage
    bridge_dmg = BridgeDamage(client)

    # Load input datasets
    bridge_dmg.load_remote_input_dataset("bridges", bridge_dataset_id)

    # Load fragility mapping
    fragility_service = FragilityService(client)
    mapping_set = MappingSet(fragility_service.get_mapping(mapping_id))
    bridge_dmg.set_input_dataset('dfr3_mapping_set', mapping_set)

    # Set analysis parameters
    bridge_dmg.set_parameter("result_name", "bridge_result")
    bridge_dmg.set_parameter("hazard_type", hazard_type)
    bridge_dmg.set_parameter("hazard_id", hazard_id)
    bridge_dmg.set_parameter("num_cpu", 4)

    # Run bridge damage analysis
    bridge_dmg.run_analysis()

    ###################################################################
    # Test liquefaction

    # south carolina eq damage
    hazard_type = "earthquake"
    hazard_id = "5ee9309bc9f1b70008fdbd26"

    # south carolina bridges
    bridge_dataset_id = "5ee92f884210b80008f9377e"

    # Default Bridge Fragility Mapping on incore-service
    mapping_id = "5b47bcce337d4a37755e0cb2"

    # Use hazard uncertainty for computing damage
    use_hazard_uncertainty = False
    # Use liquefaction (LIQ) column of bridges to modify fragility curve
    use_liquefaction = True

    # Create bridge damage
    bridge_dmg = BridgeDamage(client)

    # Load input datasets
    bridge_dmg.load_remote_input_dataset("bridges", bridge_dataset_id)

    # Load fragility mapping
    fragility_service = FragilityService(client)
    mapping_set = MappingSet(fragility_service.get_mapping(mapping_id))
    bridge_dmg.set_input_dataset('dfr3_mapping_set', mapping_set)

    # Set analysis parameters
    bridge_dmg.set_parameter("result_name", "bridge_result_w_liquefaction")
    bridge_dmg.set_parameter("hazard_type", hazard_type)
    bridge_dmg.set_parameter("hazard_id", hazard_id)
    bridge_dmg.set_parameter("use_liquefaction", use_liquefaction)
    bridge_dmg.set_parameter("num_cpu", 1)

    # Run bridge damage analysis
    bridge_dmg.run_analysis()


if __name__ == '__main__':
    run_with_base_class()
