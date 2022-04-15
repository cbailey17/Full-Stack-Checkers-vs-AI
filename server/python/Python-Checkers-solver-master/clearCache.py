#! /usr/bin/python3
"""
@author: Cameron Bailey
"""

import importlib  # import imp
import redis

redis = redis.Redis(host='localhost',
                    port=6379,
                    db=0)


def clear():
    redis.flushdb()
    print("***Database flushed***")


if __name__ == "__main__":
    clear()
