import json
import os

from source.application.csv_to_space_separate_application import CsvToSpaceSeparateApplication
from source.infrastructure.s3_csv_cash_transaction_repository import S3CsvCashTransactionRepository
from source.infrastructure.s3_shop_sales_repository import S3ShopSalesRepository
from source.util.util import get_logger, logging_decorator
from tests.in_memory_code_repository import InMemoryCodeRepository

logger = get_logger('INFO')


@logging_decorator
def import_handler(event, context):

    try:
        # Request受け取り
        body_str = event['body']
        body = json.loads(body_str)
        key = body['key']
        bucket_name = os.environ['BUCKET_NAME']

        # 変換処理の前準備(Repositoryの用意)
        code_repository = InMemoryCodeRepository()
        csv_repository = S3CsvCashTransactionRepository(key, bucket_name)
        # bucketは既に決まっている想定
        shop_sales_repository = S3ShopSalesRepository('xxxxx-bucket')

        # CSV取り込み→スペース区切り保存
        trans_app = CsvToSpaceSeparateApplication(code_repository, csv_repository, shop_sales_repository)
        trans_app.csv_to_space_separate()

        # Response組み立て
        dict_value = {'message': 'uploadしました', }
        json_str = json.dumps(dict_value)

        return {
            'statusCode': 200,
            'body': json_str
        }

    except ValueError as error:
        logger.exception(f'{error}')

        dict_value = {'message': f'{error}', }
        json_str = json.dumps(dict_value)

        return {
            'statusCode': 500,
            'body': json_str
        }
    except Exception as error:
        logger.exception(f'{error}')

        dict_value = {'message': f'処理エラーが発生しました。しばらくしてから再実行して下さい', }
        json_str = json.dumps(dict_value)

        return {
            'statusCode': 500,
            'body': json_str
        }
