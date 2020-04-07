import json
import logging
import math
import os
import unittest

import tools.process_log as process_log

TMP_LOG = '/tmp/igor_test_log.log'

logging.basicConfig(filename=TMP_LOG)

logger = logging.getLogger('Igor')
logger.setLevel(logging.DEBUG)

class TestProcessLog(unittest.TestCase):
    def setUp(self):
        # Create a dum:wmy log
        logger.error("A test error")
        logger.warning('A test warning')
        for x in range(100):
            t = x * 1/100.
            data = {
                'timestamp': t,
                'set_throttle': math.sin(t),
                'control_angle': math.cos(t)
            }
            logger.debug('Control Data: {}'.format(json.dumps(data)))

    def tearDown(self):
        os.remove(TMP_LOG)

    def test_process_log(self):
        process_log.process(TMP_LOG) 
        

        


if __name__ == "__main__":
    unittest.main()

