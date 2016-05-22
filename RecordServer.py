#!/usr/bin/env python

import socket
import struct
import sqlite3
import os

HOST = "127.0.0.1"
PORT = 8390
DBFILE = "/opt/ProxyAnalyze/var/analyze.db"

SFMT = '>h'
IFMT = '>I'


def BytesToNumber(fmt, message, offset):
    num = struct.unpack_from(fmt, message, offset)[0]
    offset += struct.calcsize(fmt)
    return num, offset


class RecordInfo(object):
    def __init__(self):
        self.version = 0
        self.s_sec = 0
        self.s_usec = 0
        self.e_sec = 0
        self.e_usec = 0
        self.ip = 0
        self.port = 0
        self.upload = 0
        self.download = 0
        self.user = ''
        self.host = ''


    def ParseFrom(self, message):
        offset = 0

        self.version, offset = BytesToNumber(SFMT, message, offset)

        self.s_sec, offset = BytesToNumber(IFMT, message, offset)
        self.s_usec, offset = BytesToNumber(IFMT, message, offset)
        self.e_sec, offset = BytesToNumber(IFMT, message, offset)
        self.e_usec, offset = BytesToNumber(IFMT, message, offset)
        self.ip, offset = BytesToNumber(IFMT, message, offset)
        self.port, offset = BytesToNumber(IFMT, message, offset)
        self.upload, offset = BytesToNumber(IFMT, message, offset)
        self.download, offset = BytesToNumber(IFMT, message, offset)

        user_len, offset = BytesToNumber(SFMT, message, offset)
        self.user = message[offset : offset + user_len].decode('ascii')
        offset += user_len

        host_len, offset = BytesToNumber(SFMT, message, offset)
        self.host = message[offset : offset + host_len].decode('ascii')
        offset += host_len
        

    def PrintDebug(self):
        outstr = "\
STime: {1},{2}{0}\
ETime: {3},{4}{0}\
User: {5}{0}\
Connect: {6},{7}{0}\
Host: {8}{0}\
Upload: {9}{0}\
Download: {10}{0}\
".format(os.linesep,
        self.s_sec, self.s_usec,
        self.e_sec, self.e_usec,
        self.user,
        socket.inet_ntoa(struct.pack("=I", self.ip)), self.port,
        self.host,
        self.upload, self.download)
        print outstr


    def InsertSql(self):
        sql = "INSERT INTO t_connection (\
                    version, \
                    s_sec, s_usec, e_sec, e_usec, \
                    ip, port, upload, download, \
                    user, host \
               ) VALUES (?, \
                    ?, ?, ?, ?, \
                    ?, ?, ?, ?, \
                    ?, ? \
               )"
        params = (self.version,
                  self.s_sec, self.s_usec, self.e_sec, self.e_usec,
                  self.ip, self.port, self.upload, self.download,
                  self.user, self.host)
        '''
        sql = "INSERT INTO t_connection (version) values (?)"
        params = (self.version,)
        '''
        return sql, params


    @classmethod
    def CreateSql(cls):
        return "CREATE TABLE IF NOT EXISTS t_connection (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    version INTEGER, \
                    s_sec INTEGER, \
                    s_usec INTEGER, \
                    e_sec INTEGER, \
                    e_usec INTEGER, \
                    ip INTEGER, \
                    port INTEGER, \
                    upload INTEGER, \
                    download INTEGER, \
                    user TEXT, \
                    host TEXT\
                )"


class SqliteWriter(object):
    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile)
        self.conn.execute(RecordInfo.CreateSql())
        self.conn.commit()


    def Write(self, info):
        sql, params = info.InsertSql()
        self.conn.execute(sql, params)
        self.conn.commit()


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    w = SqliteWriter(DBFILE)

    while 1:
        message = s.recv(4096)

        info = RecordInfo()
        info.ParseFrom(message)

        # info.PrintDebug()
        w.Write(info)
