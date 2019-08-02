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


def bulk_insert_books(data):
    connection = pymysql.connect(**properties)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO `books` (`id`) VALUES (%s)"
            cursor.executemany(sql, data)
        connection.commit()
    finally:
        connection.close()