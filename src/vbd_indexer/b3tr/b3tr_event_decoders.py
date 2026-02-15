from eth_abi.abi import decode
from eth_utils.address import to_checksum_address

from vbd_indexer.b3tr.b3tr_models import B3TRRewardRawEvent


def decode_reward_event(log: dict) -> B3TRRewardRawEvent:
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
    # return event
    return B3TRRewardRawEvent(
        block_number=log["meta"]["blockNumber"],
        timestamp=log["meta"]["blockTimestamp"],
        amount=reward_amount,
        receiver_address=receiver_address,
        proof=reward_proof,
        appId=app_id,
        distributor_address=distributor_address,
    )
