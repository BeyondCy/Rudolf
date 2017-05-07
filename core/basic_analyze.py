#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Rudolf Sandbox
# version = 0.1
# author = felicitychou
# email = felicitychou@hotmail.com

# standard
import binascii
import hashlib
import os
import subprocess
import sys
sys.path.append("..")

# third
import magic
import ssdeep

# self
from utils.ELFParser import ELF

class BasicAnalyzer(object):

    def __init__(self,filepath,logger,conf):

        self.filepath = filepath
        self.logger = logger
        self.conf = conf
        self.run()

    def run(self):

        try:
            # get basic info
            self.filename = os.path.basename(self.filepath)
            self.filetype = magic.from_file(self.filepath)
            self.filesize = int(os.path.getsize(self.filepath))
            # get hash
            self.md5 = self.hash_file('md5')
            self.sha256 = self.hash_file('sha256')
            self.crc32 = self.get_crc32()
            self.ssdeep = self.get_ssdeep()

            # get strings
            self.get_strings()
            self.strings = {"ascii":self.ascii_strings,"unicode":self.unicode_strings}

            # get packer info (self.packer)
            self.packer = None
            self.get_packer_info()

            # get elf info (self.elf_info)
            if -1 != self.filetype.find('ELF'):
                self.get_elf_info()
            else:
                self.elf_info = None
        except Exception as e:
            self.logger.exception('%s: %s' % (Exception, e))

    # output list
    def output(self):
        #return ['filename','filetype','filesize','md5','sha256','crc32','ssdeep','strings','packer','elf_info']
        return {
            'filename':self.filename,
            'filetype':self.filetype,
            'filesize':self.filesize,
            'md5':self.md5,
            'sha256':self.sha256,
            'crc32':self.crc32,
            'ssdeep':self.ssdeep,
            'strings':self.strings,
            'packer':self.packer,
            'elf_info':self.elf_info,
        }

    # get packer info:
    def get_packer_info(self):
        # ELF (UPX)
        cmd = [self.conf["UPX_Path"],"-q", "-t",self.filepath]
        output = subprocess.getoutput(cmd)
        if -1!=output.find("[OK]"):
            self.packer = "upx"
        else:
            self.packer = None
    
    # get elf info
    def get_elf_info(self):
        self.elf_info = {}
        elffile  = ELF(self.filepath)

        self.elf_info['header'] = elffile.OutputELFHeader()
        self.elf_info['section_headers'] = elffile.OutputELFShdr()
        self.elf_info['segment_headers'] = elffile.OutputELFPhdr()


    # get strings unicode and ascii 
    def get_strings(self):
        # linux return string list
        try:
            self.ascii_strings = subprocess.check_output(["strings", "-a", self.filepath]).decode().splitlines()
            self.unicode_strings = subprocess.check_output(["strings", "-a", "-el", self.filepath]).decode().splitlines()
        except Exception as e:
            self.logger.exception('%s: %s' % (Exception, e))

    # get hash ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512')
    def hash_file(self, hash_type):
        try:
            hash_handle = getattr(hashlib, hash_type)()
            with open(self.filepath, 'rb') as file:
                hash_handle.update(file.read())
            return hash_handle.hexdigest()
        except Exception as e:
            self.logger.exception('%s: %s' % (Exception, e))
        
    # get crc32
    def get_crc32(self):
        try:
            with open(self.filepath, 'rb') as file:
                return '%x' % (binascii.crc32(file.read()) & 0xffffffff)
        except Exception as e:
            self.logger.exception('%s: %s' % (Exception, e))

    # get ssdeep
    def get_ssdeep(self):
        try:
            return ssdeep.hash_from_file(self.filepath)
        except Exception as e:
            self.logger.exception('%s: %s' % (Exception, e))
