from dataclasses import dataclass
from decimal import Decimal

from indexer import IndexedEvent


@dataclass(frozen=True)
class B3TRRewardEvent(IndexedEvent):
    """
    Data gathered from the "RewardDistributed" solidity event
    """

    amount: Decimal
    appId: str
    receiver_address: str
    proof: str
    distributor_address: str
