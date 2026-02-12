from dataclasses import dataclass


@dataclass(frozen=True)
class IndexedEvent:
    """
    Base type for an indexed event
    """

    block_number: int
    timestamp: int
    tx_id: str
    clause_index: int
