# -*- coding: utf-8 -*-
import pymysql


properties = dict()
properties['host'] = '10.0.13.230'
properties['port'] = 3306
properties['user'] = 'root'
properties['password'] = 'anluda@1234'
properties['db'] = 'douban'
properties['charset'] = 'utf8mb4'
properties['cursorclass'] = pymysql.cursors.SSCursor


def query(sql):
    conn = pymysql.connect(**properties)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(e)
        results = []
    finally:
        conn.close()
    return results
