from dataclasses import asdict
from typing import List

import pandas as pd
from loguru import logger

from vbd_indexer.b3tr.b3tr_impact_names import B3TR_IMPACT_NAMES
from vbd_indexer.b3tr.b3tr_models import B3TRRewardEvent


def _analyse_rewards(rewards: List["B3TRRewardEvent"]) -> pd.DataFrame:
    """
    Runs analysis on the list of rewards and returns a per-app summary.
    """
    # convert to DataFrame (impact dict expands to impact_<name>)
    records = [asdict(e) for e in rewards]
    df = pd.json_normalize(records, sep="_")

    # Ensure amount is numeric (common if you stored Decimal as str)
    df["amount"] = pd.to_numeric(df["amount"])

    # build impact aggregations
    impact_aggs = {
        f"{name}_total": (f"impact_{name}", "sum") for name in B3TR_IMPACT_NAMES
    }

    # per-app summary
    summary_df = df.groupby("app_name", as_index=False).agg(
        actions_total=("app_name", "size"),
        wallets_unique=("receiver_address", "nunique"),
        rewards_total=("amount", "sum"),
        **impact_aggs,
    )

    # wallet action counts per app
    wallet_counts = pd.DataFrame(
        df.groupby(["app_name", "receiver_address"], as_index=False).agg(
            action_count=("receiver_address", "size")
        )
    )

    # bucket wallets by their action_count
    wallet_counts["bucket"] = pd.cut(
        wallet_counts["action_count"],
        bins=[0, 1, 5, 10, float("inf")],
        labels=[
            "wallets_one_action",
            "wallets_1_to_5_actions",
            "wallets_5_to_10_actions",
            "wallets_greater_than_10_actions",
        ],
        right=True,
        include_lowest=True,
    )

    # count wallets per bucket per app, pivot to columns
    bucket_df = (
        wallet_counts.groupby(["app_name", "bucket"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # ensure consistent columns always exist
    expected = [
        "wallets_one_action",
        "wallets_1_to_5_actions",
        "wallets_5_to_10_actions",
        "wallets_greater_than_10_actions",
    ]
    for col in expected:
        if col not in bucket_df.columns:
            bucket_df[col] = 0

    bucket_df = bucket_df[["app_name"] + expected]

    # merge buckets into main summary
    out = summary_df.merge(bucket_df, on="app_name", how="left")
    return out


def create_rewards_summary(rewards: List[B3TRRewardEvent], file_name: str) -> None:
    """
    Runs the analysis on the list of reward events for a round
    Saves the analysis to specified json file
    """
    logger.info("Running rewards analysis")
    try:
        df = _analyse_rewards(rewards)
        df.to_json(file_name, orient="records", indent=2)
        logger.info(f"Analysis saved to file: {file_name}")
    except Exception as e:
        logger.error(f"Error in rewards analysis: {e}")
        raise e
