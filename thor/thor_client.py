import time
from typing import Callable, List, Optional

import httpx

from indexer.indexed_event import IndexedEvent
from thor.thor_client_options import ThorClientOptions


class ThorClient:
    def __init__(self, options: ThorClientOptions) -> None:
        self.options = options
        self._client: Optional[httpx.Client] = httpx.Client(
            base_url=self.options.thor_url, timeout=self.options.http_request_timeout
        )

    def dispose(self) -> None:
        """
        Dispose the http client
        """
        if self._client is not None:
            self._client.close()
            self._client = None

    def get_events(
        self,
        from_block: int,
        to_block: int,
        contract_address: str,
        topic0: str,
        max_events_per_request: int,
        delay_between_requests: int,
        event_decoder: Callable[[dict], IndexedEvent],
    ) -> List[IndexedEvent]:
        """
        Post requests to thor to get the events
        Each request is for max_events_per_request events, so pagination is used to get all events
        Between requests the current thread is paused for delay_between_requests (secs), to avoid rate limiting
        Errors are not caught here, they go back to the caller
        """
        if self._client is None:
            raise RuntimeError("ThorClient is disposed")
        offset = 0
        all_pages_received = False
        all_events: List[IndexedEvent] = []
        while not all_pages_received:
            # get events for page
            page_events = self._send_get_events(
                from_block,
                to_block,
                contract_address,
                topic0,
                max_events_per_request,
                offset,
                event_decoder,
            )
            # add to all paged events
            all_events.extend(page_events)
            # check if last page
            if len(page_events) < max_events_per_request:
                all_pages_received = True
            else:
                offset = offset + max_events_per_request
            # delay between requests
            time.sleep(delay_between_requests)
        return all_events

    def _send_get_events(
        self,
        from_block: int,
        to_block: int,
        contract_address: str,
        topic0: str,
        max_events: int,
        offset: int,
        event_decoder: Callable[[dict], IndexedEvent],
    ) -> List[IndexedEvent]:
        """
        Makes a single request to thor to get events
        """
        if self._client is None:
            raise RuntimeError("ThorClient is disposed")
        # build post data
        post_data = {
            "range": {"unit": "block", "from": from_block, "to": to_block},
            "options": {"offset": offset, "limit": max_events, "includeIndexes": True},
            "criteriaSet": [{"address": contract_address, "topic0": topic0}],
        }
        # do http post
        response = self._client.post("/logs/event", json=post_data)
        response_json = response.json()
        # process events from response
        events: List[IndexedEvent] = []
        for event in response_json:
            events.append(event_decoder(event))
        return events
