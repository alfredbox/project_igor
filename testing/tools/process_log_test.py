import json
import logging
import math
import os
import tempfile
import unittest

import tools.process_log as process_log

logger = logging.getLogger('igor')
logger.setLevel(logging.DEBUG)

class TestProcessLog(unittest.TestCase):
    def setUp(self):
        # Create a dum:wmy log
        self.log = tempfile.NamedTemporaryFile(suffix='igor_test_log.log')   
        logging.basicConfig(filename=self.log)
        logger.error("A test error")
        logger.warning('A test warning')
        for x in range(100):
            t = x * 1/100.
            data = {
                'timestamp': t,
                'set_throttle': math.sin(t),
                'control_angle': math.cos(t),
                'control_d_angle': math.cos(2*t)
            }
            logger.debug('Control Data: {}'.format(json.dumps(data)))

        for x in range(100):
            t = x * 1/100.
            data = {
                'timestamp': t,
                'port_rpm': math.sin(t),
                'sbrd_rpm': math.cos(t)
            }
            logger.debug('Motor Speed Data: {}'.format(json.dumps(data)))

    def tearDown(self):
       self.log.close()

    def test_process_log(self):
        process_log.process(self.log.name, plot=False) 
        

        


if __name__ == "__main__":
    unittest.main()

