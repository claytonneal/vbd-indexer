from dataclasses import dataclass
from typing import Callable

from .indexed_event import IndexedEvent


@dataclass(frozen=True)
class ContractEvent:
    """
    Defines an index-able event detals
    """

    event_name: str
    contract_address: str
    solidity_signature: str
    topic0: str
    event_decoder: Callable[[dict, int], IndexedEvent]
