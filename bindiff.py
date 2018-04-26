#!/usr/bin/env python

'''
@author: Adel Daouzli
'''

import os
import sys
import argparse


class CompareFiles:
    # Comparing two binary files

    def __init__(self, file1, file2, fix):
        '''Get the files to compare and initialise message, offset and diff list.
        :param file1: a file
        :type file1: string
        :param file2: an other file to compare
        :type file2: string
        '''

        self._buffer_size = 2048

        # message of diff result: "not found", "size", "content", "identical"
        self.message = None

        # offset where files start to differ
        self.offset = None

        # list of diffs made of tuples: (offset, hex(byte1), hex(byte2))
        self.diff_list = []

        self.offset_differs = None

        self.file1 = file1
        self.file2 = file2

        self.fix = fix

    @property
    def compare(self):
        '''Compare the two files
        :returns: Comparison result: True if similar, False if different.
        Set vars offset and message if there's a difference.
        '''

        self.message = None
        self.offset_differs = None
        offset = 0
        offset_diff = 0
        first = False

        if not os.path.isfile(self.file1) or not os.path.isfile(self.file2):
            self.message = "not found"
            return False
        if os.path.getsize(self.file1) != os.path.getsize(self.file2):
            self.message = "size"
            # return False

        result = True
        f1 = open(self.file1, 'rb')
        f2 = open(self.file2, 'rb')
        if self.fix:
            fout = open('out.bin', 'wb+')

        loop = True
        while loop:
            buffer1 = f1.read(self._buffer_size)
            buffer2 = f2.read(self._buffer_size)

            if self.fix:
                if len(buffer1) <= len(buffer2):
                    buffer3 = bytearray(buffer1)
                else:
                    buffer3 = bytearray(buffer2)

            if len(buffer1) == 0 or len(buffer2) == 0:
                loop = False

            # for e in range(len(list(zip(buffer1, buffer2)))):
            for e in range(min(len(buffer1), len(buffer2))):
                if buffer1[e] != buffer2[e]:
                    if not first:
                        first = True
                    result = False
                    self.diff_list.append((hex(offset),
                                           hex(buffer1[e]),
                                           hex(buffer2[e])))
                    if self.fix:
                        if buffer1[e] == 0x3F:
                            buffer3[e] = buffer2[e]

                offset += 1
                if not first:
                    offset_diff += 1

            if self.fix:
                fout.write(buffer3)

        f1.close()
        f2.close()
        if self.fix:
            fout.close()

        if not result:
            if self.message is not None:
                self.message += ' + content'
            else:
                self.message = 'content'
            self.offset = hex(offset_diff)
        else:
            self.message = 'identical'

        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare Binary Files - (c) Adel Daouzli, 2018 Shp')
    parser.add_argument('file1', help='the first input file name')
    parser.add_argument('file2', help='the second input file name')
    parser.add_argument('-l', '--list', help='list all differences with offsets', action="store_true")
    parser.add_argument('-f', '--fix', help='fix 0x3F values with good ones if any', action="store_true")
    args = parser.parse_args()
    # print(args.file1)
    # print(args.file2)

    '''
    if 2 < len(sys.argv) < 5:
        if len(sys.argv) > 3:
            if sys.argv[1].strip() == '-l':
                ls = True
                f1 = sys.argv[2]
                f2 = sys.argv[3]
            else:
                # help_msg(os.path.basename(sys.argv[0]))
                parser.print_help()
                sys.exit()
        else:
            ls = False
            f1 = sys.argv[1]
            f2 = sys.argv[2]

        c = CompareFiles(f1, f2)
        result = c.compare
        print("Result of comparison: " + c.message)

        if not result and c.message.endswith('content'):
            print("offset differs: " + c.offset)
            if ls:
                print("List of differences:")
                for o, e1, e2 in c.diff_list:
                    print("offset %s: %s != %s" % (o, e1, e2))
    else:
        # help_msg(os.path.basename(sys.argv[0]))
        parser.print_help()
    '''

    c = CompareFiles(args.file1, args.file2, args.fix)
    result = c.compare
    print("Result of comparison: " + c.message)

    if not result and c.message.endswith('content'):
        print("offset differs: " + c.offset)
        if args.list:
            print("List of differences:")
            for o, e1, e2 in c.diff_list:
                print("offset %s: %s != %s" % (o, e1, e2))
