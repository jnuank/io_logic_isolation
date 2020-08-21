import decimal
import json
import logging
import traceback
from datetime import date, datetime

from pytz import timezone


def get_utc_now():
    """
    """
    utc_now = datetime.now(timezone('UTC'))
    utc_now_str = "{0:%Y-%m-%dT%H:%M:%SZ}".format(utc_now)

    return utc_now_str


def get_jst_now():
    """
    """
    jst_now = datetime.now(timezone('Asia/Tokyo'))
    jst_now_str = "{0:%Y-%m-%dT%H:%M:%S+09:00}".format(jst_now)

    return jst_now_str


class FormatterJSON(logging.Formatter):
    """
    loggerのフォーマット設定クラス
    """

    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        j = {
            'logLevel': record.levelname,
            'timestamp': '%(asctime)s.%(msecs)dZ' % dict(asctime=record.asctime, msecs=record.msecs),
            'timestamp_epoch': record.created,
            'aws_request_id': getattr(record, 'aws_request_id', '00000000-0000-0000-0000-000000000000'),
            'module': record.module,
            'filename': record.filename,
            'funcName': record.funcName,
            'levelno': record.levelno,
            'lineno': record.lineno,
            'message': record.message,
            'traceback': {},
            'extra_data': record.__dict__.get('extra_data', {}),
            'request': record.__dict__.get('request', {}),
            'response': record.__dict__.get('response', {}),
        }
        if record.exc_info:
            exception_data = traceback.format_exc().splitlines()
            j['traceback'] = exception_data

        return json.dumps(j, ensure_ascii=False)


def get_logger(level):
    """
    loggerの初期設定
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = FormatterJSON(
        '[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(levelno)s\t%(message)s\n',
        '%Y-%m-%dT%H:%M:%S'
    )
    logger.handlers[0].setFormatter(formatter)

    return logger


def logging_decorator(handler):
    """
    リクエストとレスポンスの情報をログ出力するデコレータ
    """
    def decorator(*args, **kwargs):
        logger = get_logger('INFO')

        data = {"request": args[0]}
        logger.info('Start Lambda Function', extra=dict(data))

        response = handler(*args, **kwargs)

        data = {"response": response}
        logger.info('End Lambda Function', extra=dict(data))

        return response
    return decorator


def build_response_decorator(handler):
    """
    API Gateway向けレスポンスにヘッダー情報を付与する
    """
    def decorator(*args, **kwargs):
        response = handler(*args, **kwargs)
        headers = response.get('headers', {})
        headers.update({
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key",
            "Access-Control-Allow-Credentials": "true",
            "Cache-Control": "no-cache"
        })
        response['headers'] = headers
        response['body'] = json.dumps(response.get('body', {}), default=convert_types)
        return response
    return decorator


def convert_types(obj):
    """
    型を変換する関数。
    特定の型ではjson.dumps()する際に変換が必要なためこれを使用する。
    """
    # 日付型の場合は文字列に変換
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    # Decimal型の場合はintに変換
    elif isinstance(obj, decimal.Decimal):
        return int(obj)
    # 上記以外はサポート対象外
    raise TypeError("Type {} not serializable".format(type(obj)))