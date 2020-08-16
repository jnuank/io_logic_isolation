import dataclasses

from source.util.util import get_logger

logger = get_logger('INFO')

@dataclasses
class CsvToSpaceSeparateApplication(object):
    """
    CSV→スペース区切りに変換する処理
    """
    bucket: str
    key: str

    def csv_to_space_separate(self) -> None:
        """
        CSV→スペース区切り変換
        """
        pass