# -*- coding: utf-8 -*-
import socket
import threading
import time
import unittest


# Web Server 클래스 구현
class MinWeb(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.s = None

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("localhost", self.port))
        self.s.listen(1)
        while 1:
            try:
                conn, addr = self.s.accept()
                recvmsg = conn.recv(1024)
                conn.send(self.simpleResponse(recvmsg))
                conn.close()

            except socket.error:
                break

    def simpleResponse(self, msg):
        return """HTTP/1.1 200 OK
Server: SimpleHTTPServer
Content-type: text/plain
Content-Length: %s
%s""" % (len(msg), msg)

    def stop(self):
        if self.s:
            self.s.cloase()
        self.join()


# Test Case 구현
class TestMinWeb(unittest.TestCase):
    def setUp(self):
        self.server = MinWeb(port=8080)
        self.server.start()

    def tearDown(self):
        time.sleep(0.5)
        self.server.stop()

    def test1(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 8080))
        s.send("abc")
        self.assertEqual(self.server.simpleResponse("abc"), s.recv(1024))
        s.close()


if __name__ == "__main__":
    MinWeb(port=8080).start()
# TODO ERR_CONTENT_LENGTH_MISMATCH (에러 수정 필요)