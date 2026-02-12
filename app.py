from b3tr import B3TR_REWARD_DEFINITION
from indexer import EventIndexer, IndexerOptions

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    # create indexer options
    b3tr_reward_def = B3TR_REWARD_DEFINITION
    options = IndexerOptions(
        block_start=23948404,
        block_end=23948404 + 60479,
        contract_address=b3tr_reward_def.contract_address,
        topic0=b3tr_reward_def.topic0,
        thor_endpoints=[
            "https://mainnet.vechain.org",
            "https://mainnetc1.vechain.network",
            "https://mainnetc2.vechain.network",
            "https://mainnet.vecha.in",
            "https://vethor-node.vechain.com",
            "https://node.vechain.energy",
            "https://sync-mainnet.vechain.org",
        ],
        task_block_size=240,
        delay_between_thor_requests=0.2,
        max_events_per_thor_request=1000,
        event_decoder=b3tr_reward_def.event_decoder,
    )

    # create event indexer
    idx = EventIndexer(options)

    idx.start()
    final_status = idx.wait()  # blocks until done (or failed/stopped)
    print("Final status:", final_status)

    if idx.error:
        print("Error:", repr(idx.error))

    completed, total = idx.progress()
    print(f"Progress: {completed}/{total}")
    print("Results count:", len(idx.results()))

    idx.write_to_csv_file("events.csv")
