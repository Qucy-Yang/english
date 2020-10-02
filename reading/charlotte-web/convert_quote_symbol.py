# -*- coding: utf-8 -*-

# This script is converting normal " symoble into TeX's quote symbol like ``''
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class QuoteConverter:
    __fn = ''
    __test_data = '"That\'s good," said mom\nBut I said,"you are\nnot correct". Haha'
    __quote_started = False

    def __init__(self, fn):
        self.__fn = fn

    def run(self):
        count = 0 # we will try replace with tail section..
        fd = open('./new.tex', 'w')
        with open('./charlottes.web.tex', 'r') as f:
            for line in f:
                count = count + 1
                if count > 1000:
                    new_line = self.replace_quote(line)
                    fd.write(new_line)
                else:
                    fd.write(line)
        return 0

    # return the converted line if it existed
    def replace_quote(self, line):
        new_line = ''

        for i in line:

            if i == '"': # here we go
                if self.__quote_started == False:
                    # the first meet case
                    new_line = new_line + '``'
                    self.__quote_started = True

                elif self.__quote_started == True:
                    new_line = new_line + '\'\''
                    self.__quote_started = False
            else:
                new_line = new_line + i

        return new_line

    def unit_test(self):
        each_line = self.__test_data.split('\n')

        print("The whole test data are:\n")
        for it in each_line:
            print(it)
            new_line =  self.replace_quote(it)
            print("\n======\nnew:%s\nold:%s" %(new_line, it))

        return 0



## trigger here
cv = QuoteConverter('./charlottes.web.tex')
cv.run()
