from dataclasses import dataclass
from typing import Callable, List

from .indexed_event import IndexedEvent


@dataclass(frozen=True)
class IndexerOptions:
    """
    Indexer options
    """

    round_number: int
    contract_address: str
    topic0: str
    thor_endpoints: List[str]
    task_block_size: int
    max_events_per_thor_request: int
    delay_between_thor_requests: float
    event_decoder: Callable[[dict], IndexedEvent]
    event_transformer: Callable[[IndexedEvent], IndexedEvent]
