from eth_abi.abi import decode
from eth_utils.address import to_checksum_address

from b3tr.b3tr_reward_event import B3TRRewardEvent
from utils.units import format_wei

from .b3tr_apps import get_app_name


def decode_reward_event(log: dict, round_number: int) -> B3TRRewardEvent:
    """
    Decodes an event to a B3TRRewardEvent class
    This event has signature:
    event RewardDistributed(
      uint256 amount,
      bytes32 indexed appId,
      address indexed receiver,
      string proof,
      address indexed distributor
    );
    """
    data = log["data"]
    topics = log["topics"]
    # indexed data
    app_id = topics[1]
    receiver_address = to_checksum_address("0x" + topics[2][-40:])
    distributor_address = to_checksum_address("0x" + topics[3][-40:])
    # --- non-indexed fields from data ---
    # order: uint256 amount, string proof
    reward_amount, reward_proof = decode(
        ["uint256", "string"],
        bytes.fromhex(data[2:]),
    )
    # convert b3tr wei to b3tr units
    reward_b3tr = format_wei(reward_amount)
    # map app id to app name
    app_name = get_app_name(app_id, round_number)
    # return event
    return B3TRRewardEvent(
        block_number=log["meta"]["blockNumber"],
        timestamp=log["meta"]["blockTimestamp"],
        tx_id=log["meta"]["txID"],
        clause_index=log["meta"]["clauseIndex"],
        amount=reward_b3tr,
        receiver_address=receiver_address,
        proof=reward_proof,
        appId=app_id,
        app_name=app_name,
        distributor_address=distributor_address,
    )
