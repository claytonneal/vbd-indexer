from dataclasses import dataclass
from decimal import Decimal
from typing import Dict

from vbd_indexer.indexer.indexed_event import IndexedEvent

# ---------------------------
# Indexed Event objects
# ---------------------------


@dataclass(frozen=True)
class B3TRRewardRawEvent(IndexedEvent):
    """
    Data gathered from the direct decoding of a "RewardDistributed" solidity event
    """

    amount: int
    appId: str
    receiver_address: str
    proof: str
    distributor_address: str


# -----------------------------
# Transformed Event objects
# -----------------------------


@dataclass(frozen=True)
class B3TRRewardEvent(IndexedEvent):
    """
    A transformed/sanitised B3TRRewardRawEvent
    """

    amount: Decimal
    app_id: str
    app_name: str
    receiver_address: str
    impact: Dict[str, Decimal]
