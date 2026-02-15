import fire
from loguru import logger

from vbd_indexer.analysis.reward_analyser import create_rewards_summary
from vbd_indexer.b3tr.b3tr_apps import warm_app_name_cache
from vbd_indexer.b3tr.b3tr_events_defs import B3TR_REWARD_DEFINITION
from vbd_indexer.b3tr.b3tr_models import B3TRRewardDecodedEvent, B3TRRewardEvent
from vbd_indexer.indexer.event_indexer import EventIndexer
from vbd_indexer.indexer.indexer_options import IndexerOptions

# -----------------------------
# Logo printer
# -----------------------------


def print_logo() -> None:
    print("""
        ▗▖  ▗▖▗▄▄▖ ▗▄▄▄     ▗▄▄▄▖▗▖  ▗▖▗▄▄▄ ▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖▗▄▄▖
        ▐▌  ▐▌▐▌ ▐▌▐▌  █      █  ▐▛▚▖▐▌▐▌  █▐▌    ▝▚▞▘ ▐▌   ▐▌ ▐▌
        ▐▌  ▐▌▐▛▀▚▖▐▌  █      █  ▐▌ ▝▜▌▐▌  █▐▛▀▀▘  ▐▌  ▐▛▀▀▘▐▛▀▚▖
         ▝▚▞▘ ▐▙▄▞▘▐▙▄▄▀    ▗▄█▄▖▐▌  ▐▌▐▙▄▄▀▐▙▄▄▖▗▞▘▝▚▖▐▙▄▄▖▐▌ ▐▌


        """)


# -----------------------------
# Index Rewards
# -----------------------------


def index_rewards(round_id: int) -> None:
    if round_id < 1:
        raise ValueError("round_id has to be >= 1")
    # create indexer options
    b3tr_reward_def = B3TR_REWARD_DEFINITION
    options = IndexerOptions[B3TRRewardDecodedEvent, B3TRRewardEvent](
        round_number=round_id,
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
        event_transformer=b3tr_reward_def.event_transformer,
    )
    # pre-warm the app name cache
    warm_app_name_cache(round_id)
    # create event indexer
    idx = EventIndexer(options)
    idx.start()
    final_status = idx.wait()  # blocks until done (or failed/stopped)
    logger.info(f"Final status: {final_status}")
    if idx.error:
        logger.error("Error:", repr(idx.error))
    completed, total = idx.progress()
    logger.info(f"Progress: {completed}/{total}")
    logger.info(f"Results count: {len(idx.results())}")
    idx.write_to_csv_file(f"rewards-events-round-{round_id}.csv")
    # do the analysis
    create_rewards_summary(
        idx.results(), f"reward-events-summary-round-{round_id}.json"
    )


# -----------------------------
# Entry point
# -----------------------------


def main() -> None:
    print_logo()
    fire.Fire(index_rewards)


if __name__ == "__main__":
    main()
