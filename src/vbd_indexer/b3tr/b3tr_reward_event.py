from dataclasses import dataclass
from decimal import Decimal

from vbd_indexer.indexer import IndexedEvent


@dataclass(frozen=True)
class B3TRRewardEvent(IndexedEvent):
    """
    Data gathered from the "RewardDistributed" solidity event
    """

    amount: Decimal
    appId: str
    app_name: str
    receiver_address: str
    proof: str
    distributor_address: str
