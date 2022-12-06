'''
在之前的项目中，代码中都暴露了一些隐私的信息，例如连接数据库等连接信息。
本节就是讲解在fastapi中如何不暴露这些信息
'''
'''
方法1：
将隐私信息存放在系统的环境变量中
'''
import os
def get_dburl_from_env(key):
    '''
    获取系统环境变量中名为key的变量值，
    当不存在时返回None
    :param key:为变量名
    :return :key对应的value，不存在时返回None
    '''
    value = os.getenv(key,None)
    return value

class NoValueException(Exception):
    pass

if __name__ == "__main__":
    db_url = get_dburl_from_env("DBURL")
    if db_url is None:
        raise NoValueException
    print(db_url)
    test_url = get_dburl_from_env("TEST")
    if test_url is None:
        raise NoValueException
    print(test_url)
    