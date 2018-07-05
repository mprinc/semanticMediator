#!/usr/bin/python3

# requirements
import unittest
import requests
import logging
import json
import yaml
import sys
import os

class MediatorTests(unittest.TestCase):

    config = None
    statsURI = None
    clearStatsURI = None
    
    @classmethod
    def setUpClass(self):

        # read config file
        try:        
            self.config = os.environ["MEDIATORTEST"]
        except KeyError:
            logging.error("You must specify a configuration file through the variable $MEDIATORTEST")
            sys.exit()            
        yf = open(self.config, "r")
        ym = yaml.load(yf)        
        self.mediatorBaseURI = ym["mediator"]["baseUri"]
        self.trackSearchPath = ym["mediator"]["routes"]["trackSearch"]["path"]
        self.trackSearchArgs = ym["mediator"]["routes"]["trackSearch"]["args"]

        # close file
        yf.close()

        
    def test_00_successful_track_search(self):

        # request configuration
        reqConf = {"pattern": "barking"}
        params = None

        # build URI
        for arg in self.trackSearchArgs:
            if not params:
                params = "?%s=%s" % (arg, reqConf[arg])
            else:
                params += "&%s=%s" % (arg, reqConf[arg])

        # make the request
        r = requests.get(self.mediatorBaseURI + self.trackSearchPath + params)
        msg = json.loads(r.text)
        
        # check that returns 200
        self.assertEqual(200, r.status_code)
        self.assertEqual("ok", msg["status"])

                
if __name__ == "__main__":
    unittest.main(verbosity = 2)