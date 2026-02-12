from eth_utils.crypto import keccak

from indexer.contract_event import ContractEvent

from .b3tr_contracts import B3TR_CONTRACTS
from .b3tr_event_decoders import decode_reward_event

B3TR_REWARD_DEFINITION: ContractEvent = ContractEvent(
    event_name="RewardDistributed",
    contract_address=B3TR_CONTRACTS["X2EarnRewardsPool"],
    solidity_signature="RewardDistributed(uint256,bytes32,address,string,address)",
    topic0=keccak(
        text="RewardDistributed(uint256,bytes32,address,string,address)"
    ).hex(),
    event_decoder=decode_reward_event,
)
