from dataclasses import dataclass

from indexer import IndexedEvent


@dataclass(frozen=True)
class B3TRRewardEvent(IndexedEvent):
    """
    Data gathered from the "RewardDistributed" solidity event
    """

    amount: int
    appId: str
    receiver_address: str
    proof: str
    distributor_address: str
