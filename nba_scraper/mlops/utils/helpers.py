from collections.abc import Iterable
from nba_scraper.mlops.pipeline.config import LastNGamesFeatures as lngf

class LastNGamesHelper:

    @staticmethod
    def filter_nth_game_features(
        column_values: Iterable[str]
    ) -> list[str]:
        try:
            return sorted([
                key for key in column_values
                if isinstance(key, str) and key.startswith(lngf.NTH_GAME_PREFIX)
            ])
        except TypeError as e:
            raise TypeError(
                f"'column_values' must be an iterable of strings, got {type(column_values)}"
            ) from e
