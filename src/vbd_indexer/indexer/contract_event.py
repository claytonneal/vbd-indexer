from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from .indexed_event import IndexedEvent

DecodedEventType = TypeVar("DecodedEventType", bound=IndexedEvent)
TransformedEventType = TypeVar("TransformedEventType", bound=IndexedEvent)


@dataclass(frozen=True)
class ContractEvent(Generic[DecodedEventType, TransformedEventType]):
    """
    Defines an index-able event detals
    """

    event_name: str
    contract_address: str
    solidity_signature: str
    topic0: str
    event_decoder: Callable[[dict], DecodedEventType]
    event_transformer: Callable[[DecodedEventType], TransformedEventType]
