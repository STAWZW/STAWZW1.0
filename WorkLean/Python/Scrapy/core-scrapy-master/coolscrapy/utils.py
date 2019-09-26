# -*- encoding: utf-8 -*-
"""
Topic: 一些工具类
Desc : 
"""
import re
import sys
from contextlib import contextmanager
from datetime import datetime
from scrapy.loader.processors import Identity, TakeFirst

@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def parse_text(extract_texts, rule_name, attr_name):
    """xpath的提取方式
    @param extract_texts: 被处理的文本数组
    @param rule_name: 规则名称
    @param attr_name: 属性名
    """
    custom_func = "%s_%s" % (rule_name, attr_name)
    if custom_func in globals():
        return globals()[custom_func](extract_texts)
    return '\n'.join(extract_texts).strip() if extract_texts else ""

def merge_list(target_list,splitter):
    return splitter.join(target_list).strip()

def time_format(datetime_str):
    releaseTime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    return releaseTime

def de_weighting_list(target_list):
    return list(set(target_list))

class Identity_overload(Identity):
    def __call__(self, values):
        if not values:
            values.append('')
        return values

class TakeFirst_overload(TakeFirst):
    def __call__(self, values):
        for value in values:
            if value is not None:
                return value