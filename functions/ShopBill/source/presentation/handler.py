import json
import os

import boto3

from source.application.csv_to_space_separate_application import CsvToSpaceSeparateApplication
from source.util.util import get_logger, logging_decorator

logger = get_logger('INFO')


@logging_decorator
def import_handler(event, context):

    try:
        # eventから必要情報を抜き出す
        body_str = event['body']
        body = json.loads(body_str)
        key = body['key']
        bucket_name = os.environ['BUCKET_NAME']

        download_filepath = '/tmp/' + key
        # S3にアップロードされたファイルをダウンロード
        try:
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(bucket_name)
            bucket.download_file(key, download_filepath)
        except Exception as error:
            raise error

        # 別のアプリケーションサービス
        # Bucket名とKey名を渡したら、欲しいCSVデータを持ってきてくれる
        # ここで失敗する可能性もある。

        # CSV取り込み→スペース区切り保存
        trans_app = CsvToSpaceSeparateApplication(bucket, key)
        trans_app.csv_to_space_separate('dummy_file.csv')

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
