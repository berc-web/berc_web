import os
import berc
import unittest
import tempfile

class bercTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, berc.app.config['DATABASE'] = tempfile.mkstemp()
        berc.app.config['TESTING'] = True
        self.app = berc.app.test_client()
        # berc.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(berc.app.config['DATABASE'])

    def test_home_page_view(self):
    	rv = self.app.get('/')
    	assert '<title>EECC2015</title>' in rv.data

if __name__ == '__main__':
    unittest.main()