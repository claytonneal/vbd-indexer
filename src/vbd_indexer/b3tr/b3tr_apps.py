from functools import lru_cache
from typing import Dict, List

from eth_abi.abi import decode, encode
from eth_utils.crypto import keccak
from loguru import logger

from vbd_indexer.b3tr.b3tr_contracts import B3TR_CONTRACTS
from vbd_indexer.thor import ThorClient, ThorClientOptions


def _fetch_apps_for_round(round_number: int) -> List[Dict]:
    """
    Gets a list of app ids and app names for the round number
    Only need to call this once and then cache it
    """
    client_options = ThorClientOptions(
        thor_url="https://mainnet.vechain.org", http_request_timeout=10
    )
    thor_client = ThorClient(client_options)
    try:
        logger.info(f"Getting app names for round {round_number}")
        # encode the function call data
        solidity_sig = "getAppsOfRound(uint256)"
        func_selector = keccak(text=solidity_sig)[:4]
        encoded_args = encode(["uint256"], [round_number])
        encoded_call_data = "0x" + (func_selector + encoded_args).hex()
        # get the raw response
        response_data = thor_client.call_contract(
            contract_address=B3TR_CONTRACTS["XAllocationVoting"],
            call_data=encoded_call_data,
        )
        # decode the response
        raw = bytes.fromhex(response_data[2:])  # strip 0x
        app_type = "(bytes32,address,string,string,uint256,bool)[]"
        apps = decode([app_type], raw)[0]
        # extract only id and name
        result = []
        for app in apps:
            app_id = "0x" + app[0].hex()
            name = app[2]
            result.append(
                {
                    "id": app_id,
                    "name": name,
                }
            )
        logger.info(f"Round {round_number} has {len(result)} active apps")
        return result

    finally:
        thor_client.dispose()


@lru_cache(maxsize=64)
def get_apps_for_round_cached(round_number: int) -> Dict[str, str]:
    """
    Cached map: app_id -> name for a given round_number.
    Only hits the chain once per round (per process).
    """
    apps = _fetch_apps_for_round(round_number)
    return {a["id"].lower(): a["name"] for a in apps}


def get_app_name(app_id: str, round_number: int) -> str:
    """
    Returns the app name for an id, using cached round data.
    If not found, returns None.
    """
    app_map = get_apps_for_round_cached(round_number)
    app_name = app_map.get(app_id.lower())
    if app_name is None:
        logger.error(f"No app name for app id {app_id}")
        raise ValueError(f"No app name for app id {app_id}")
    return app_name
