import json
import os

from source.util.util import get_logger, logging_decorator

from source.application.csv_to_space_separate_application import CsvToSpaceSeparateApplication
from source.infrastructure.s3_csv_cash_transaction_repository import S3CsvCashTransactionRepository
from source.infrastructure.s3_shop_sales_repository import S3ShopSalesRepository
from tests.In_memory_code_repository import InMemoryCodeRepository

logger = get_logger('INFO')


@logging_decorator
def import_handler(event, context):

    try:
        # eventから必要情報を抜き出す
        body_str = event['body']
        body = json.loads(body_str)
        key = body['key']
        bucket_name = os.environ['BUCKET_NAME']

        code_repository = InMemoryCodeRepository()
        csv_repository = S3CsvCashTransactionRepository(key, bucket_name)
        # アップロード先のbucketは既に決まっている想定
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
