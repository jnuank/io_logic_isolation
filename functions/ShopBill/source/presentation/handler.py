from source.infrastructure.s3_care_bill_repository import S3CareBillRepository
from source.infrastructure.s3_care_csv_bill_total_repository import S3CareCsvBillTotalRepository
from source.infrastructure.s3_care_csv_bill_repository import S3CareCsvBillRepository
from source.infrastructure.s3_code_repository import S3CodeRepository
from source.application.csv_to_space_separate_application import CsvToSpaceSeparateApplication
import os
import json
from source.util.util import get_logger, logging_decorator

logger = get_logger('INFO')


@logging_decorator
def import_handler(event, context):

    try:
        # eventから必要情報を抜き出す
        body_str = event['body']
        body = json.loads(body_str)
        key = body['key']
        bucket = os.environ['BUCKET_NAME']

        # CSV取り込み→スペース区切り保存
        trans_app = CsvToSpaceSeparateApplication(bucket, key)
        trans_app.csv_to_space_separate()

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
