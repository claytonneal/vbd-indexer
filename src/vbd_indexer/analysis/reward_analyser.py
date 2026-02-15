from dataclasses import asdict
from typing import List

import pandas as pd
from loguru import logger
from pandas import DataFrame

from vbd_indexer.b3tr.b3tr_models import B3TRRewardEvent


def _analyse_rewards(rewards: List[B3TRRewardEvent]) -> DataFrame:
    """
    Runs analysis on the list of rewards
    """
    # convert to DataFrame
    records = [asdict(e) for e in rewards]
    df = pd.json_normalize(records, sep="_")  # columns will be "impact_<name>"
    # analyse
    summary_df = (
        df.groupby("app_name")
        .agg(
            total_actions=("app_name", "size"),  # count rows
            unique_wallets=("receiver_address", "nunique"),  # distinct wallets
            total_rewards=("amount", "sum"),  # total b3tr
        )
        .reset_index()
    )
    return summary_df


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
