import json
from decimal import Decimal
from typing import Dict

from loguru import logger

# TODO - can this come from a contract call?
_impact_field_names = [
    "carbon",
    "water",
    "energy",
    "waste_mass",
    "timber",
    "plastic",
    "education_time",
    "trees_planted",
    "calories_burned",
    "sleep_quality_percentage",
    "clean_energy_production_wh",
]


def parse_reward_proof(raw_proof: str) -> Dict[str, Decimal]:
    """
    Parses a sustainability proof
    Returns a dict of impact name and value
    """
    try:
        impacts: Dict[str, Decimal] = {}
        proof_json = json.loads(raw_proof)
        if "impact" not in proof_json:
            return {name: Decimal(0) for name in _impact_field_names}
        for field_name in _impact_field_names:
            if field_name in proof_json["impact"]:
                impact_value = Decimal(proof_json["impact"][field_name])
                impacts[field_name] = impact_value
            else:
                impacts[field_name] = Decimal(0)
        return impacts
    except Exception as e:
        if raw_proof is not None and len(raw_proof) > 0:
            logger.warning(f"Unable to parse reward proof: {raw_proof}")
        return {name: Decimal(0) for name in _impact_field_names}
