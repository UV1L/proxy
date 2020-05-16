import unittest
import server as s


class MyTestCase(unittest.TestCase):

    def test_something(self):
        mb = s.parse_details(b'CONNECT queuev4.vk.com:443'
                             b' HTTP/1.1\r\nHost:'
                             b' queuev4.vk.com:443\r\nProxy-Connection:'
                             b' keep-alive\r\nUser-Agent: Mozilla/5.0 '
                             b'(Windows NT 10.0; Win64; x64) '
                             b'AppleWebKit/537.36 '
                             b'(KHTML, like Gecko)'
                             b' Chrome/73.0.3683.103 Safari/537.36'
                             b' OPR/60.0.3255.109\r\n\r\n')

        _is = {'server_port': 443,
               'server_url': b'queuev4.vk.com', 'client_data':
               b'CONNECT  HTTP/1.1\r\nHost: '
               b'queuev4.vk.com:443\r\nProxy-Connection: '
               b'keep-alive\r\nUser-Agent: Mozilla/5.0 '
               b'(Windows NT 10.0; Win64; x64)'
               b' AppleWebKit/537.36 (KHTML, like Gecko) '
               b'Chrome/73.0.3683.103 '
               b'Safari/537.36 OPR/60.0.3255.109\r\n\r\n\r\n',
               'method': b'CONNECT'}
        self.assertEqual(_is, mb)


if __name__ == '__main__':
    unittest.main()
