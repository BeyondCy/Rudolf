#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Rudolf Sandbox
# version = 0.1
# author = felicitychou
# email = felicitychou@hotmail.com

# standard
from optparse import OptionParser
from configparser import ConfigParser
import json
import time
import os

# self
from core.basic_analyze import BasicAnalyzer
from core.static_analyze import StaticAnalyzer
from core.dynamic_analyze import DynamicAnalyzer
from core.logger import Logger

# init logger
logger = Logger().logger



def analyze(filepath,mode):
    global logger
    logger.info("Analyze %s mode:%s" % (filepath, mode))

    static,dynamic = True,True
    if mode == 'static':
        dynamic = False
    elif mode == 'dynamic':
        static = False
    elif mode == 'basic':
        static,dynamic = False,False
    else:
        pass

    # get config
    config = ConfigParser()
    config.read_file(open('rudolf.cfg'))
    logger.info("Read rudolf.cfg successfully.")

    # init basic analyzer
    basic_analyzer = BasicAnalyzer(filepath = filepath,logger = logger,conf = config['basic'])
    logger.info("Init and Run basic_analyzer successfully.")
    # set result_path
    result_path = os.path.join(config.get('rudolf','Result_Path'), '%s_%s' % (basic_analyzer.sha256, time.time()))
    os.makedirs(result_path)
    logger.info("Make result path %s" % (result_path,))
    # init static analyzer
    if static:
        static_analyzer = StaticAnalyzer(filepath = filepath,hash = basic_analyzer.md5,logger = logger,conf = config['static'])
        logger.info("Init and Run static_analyzer successfully.")
    # init dynamic analyzer
    if dynamic:
        dynamic_analyzer = DynamicAnalyzer(filepath = filepath,filetype = basic_analyzer.filetype,result_path = result_path,
                                           sandbox_id = 1,logger = logger,conf = config['dynamic'])
        logger.info("Init and Run dynamic_analyzer successfully.")

    # output result
    with open(os.path.join(result_path,'basic.json'),'w') as fw:
        json.dump(basic_analyzer.output(),fw)
        logger.info("Output basic_analyzer result successfully.")
    if static:
        with open(os.path.join(result_path,'static.json'),'w') as fw:
            json.dump(static_analyzer.output(),fw)
            logger.info("Output static_analyzer result successfully.")
    if dynamic:
        with open(os.path.join(result_path,'dynamic.json'),'w') as fw:
            json.dump(dynamic_analyzer.output(),fw)
            logger.info("Output dynamic_analyzer result successfully.")


def main():
    usage = "usage: %prog [options] args"
    parser = OptionParser(version = "%prog 1.0")

    parser.add_option("-f", "--file", dest="filepath", help="Malcode filepath")
    parser.add_option("-m", "--mode", dest="mode", help="Malcode Analyze mode: basic/static/dynamic/all",default='all')

    (options, args) = parser.parse_args()

    filepath = None
    if options.filepath:
        filepath = options.filepath
    if options.mode:
        mode = options.mode

    if filepath and os.path.exists(filepath):
        analyze(filepath = filepath,mode = mode)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
