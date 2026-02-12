from eth_utils.crypto import keccak

from indexer.contract_event import ContractEvent

from .b3tr_event_decoders import decode_reward_event

B3TR_REWARD_DEFINITION: ContractEvent = ContractEvent(
    event_name="RewardDistributed",
    contract_address="0x6Bee7DDab6c99d5B2Af0554EaEA484CE18F52631",
    solidity_signature="RewardDistributed(uint256,bytes32,address,string,address)",
    topic0=keccak(
        text="RewardDistributed(uint256,bytes32,address,string,address)"
    ).hex(),
    event_decoder=decode_reward_event,
)
