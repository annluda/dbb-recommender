# -*- coding: utf-8 -*-
import pymysql

properties = dict()
properties['host'] = '10.0.13.230'
properties['port'] = 3306
properties['user'] = 'root'
properties['password'] = 'anluda@1234'
properties['db'] = 'douban'
properties['charset'] = 'utf8mb4'
properties['cursorclass'] = pymysql.cursors.DictCursor


def bulk_insert_into_books(data):
    conn = pymysql.connect(**properties)
    try:
        with conn.cursor() as cursor:
            sql = "INSERT IGNORE INTO `books` (`id`) VALUES (%s)"
            cursor.executemany(sql, data)
        conn.commit()
    finally:
        conn.close()