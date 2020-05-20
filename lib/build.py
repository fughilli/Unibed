#!/usr/bin/python

##
## Unibed is a unified embedded development platform.
## Copyright (C) 2016  Kevin Balke  (kbalke@ucla.edu)
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software Foundation,
## Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
##

import re
import os

def join_flags(flags):
    return ' '.join(flags)

class FileNamespace(object):

    @staticmethod
    def root():
        return FileNamespace(None, [])

    def __init__(self, parent, files):
        self.files = files
        self.parent = parent

    def __getFiles(self):
        if(self.parent):
            return self.parent.__getFiles() + self.files
        return self.files

    def getFiles(self, regex=None):
        if(regex == None):
            return self.__getFiles()

        regex = re.compile(regex)

        return filter(lambda f : regex.match(f), self.__getFiles())

    def hasFile(self, f):
        for x in self.__getFiles():
            if x.endswith(f):
                return True
        return False

    def hasFiles(self, fs):
        return reduce(lambda a,b : a and b, map(self.hasFile, fs))

    def addFile(self, f):
        self.files.append(f)

    def addFiles(self, fs):
        self.files.extend(fs)

def process_step(stepspec, fns):
    '''Process a build step, updating the file namespace, fns. Return the input
    and output files for this step.'''
    def parse_regex_arg(rarg):
        return ('r' in rarg[0], '*' in rarg[0], rarg[1])

    in_use_regex, in_use_multiple, in_regex = parse_regex_arg(stepspec[0])
    out_use_regex, out_use_multiple, out_regex = parse_regex_arg(stepspec[1])
    step_func = stepspec[2]

    if in_use_multiple:
        if out_use_multiple:
            if in_use_regex and out_use_regex:
                # MIMO RR

                # Get all files in the fns matching the input regex
                in_files = fns.getFiles(in_regex)

                # Get the output filenames by running a regex substitution
                out_files = [re.sub(in_regex, out_regex, x) for x in in_files]

                # Add the output files to the fns
                fns.addFiles(out_files)

                return ([[x] for x in in_files], [[x] for x in out_files], step_func)
            if not (in_use_regex or out_use_regex):
                # MIMO AA

                raise Exception("Multiple-in, multiple-out requires regex for substitution.")
        else:
            if out_use_regex:
                raise Exception("Multiple-in, single-out requires absolute output name.")

            if in_use_regex:
                # Multiple regex in, single filename out
                in_files = fns.getFiles(in_regex)

                out_file = out_regex

                fns.addFile(out_file)

                return ([in_files], [[out_file]], step_func)

            else:
                if not fns.hasFiles(in_files):
                    raise Exception("Unknown file in %s." % in_files)

                in_files = in_regex

                out_file = out_regex

                fns.addFile(out_file)

                return ([[x] for x in in_files], [[out_file]], step_func)
    else:
        if not out_use_multiple:
            if not (in_use_regex or out_use_regex):
                # SISO AA
                in_file = in_regex
                out_file = out_regex

                fns.addFile(out_file)

                return ([[in_file]], [[out_file]], step_func)

    raise Exception("Unsupported options for build step: %s, %s" % stepspec[:-1])

def __findFiles(root, regex, recurse):
    files = [os.path.join(root, x) for x in os.listdir(root)]
    retfiles = filter(lambda f : os.path.isfile(f) and regex.match(f), files)

    if recurse:
        retfiles.extend(
            reduce(lambda a,b : a+b,
            map(lambda d : __findFiles(d, regex, recurse),
            filter(lambda x : os.path.isdir(x), files)), []))

    return retfiles

def findFiles(root, regex, recurse=False):
    regex = re.compile(regex)

    return __findFiles(root, regex, recurse)

def csrc_to_obj(i_files, o_files, config):
    ret = []
    for i,o in zip(i_files, o_files):
        ret.append("%s %s -c %s -o %s" % (config['cc'], join_flags(config['ccflags']), i, o))
    return ret

def cppsrc_to_obj(i_files, o_files, config):
    ret = []
    for i,o in zip(i_files, o_files):
        ret.append("%s %s -c %s -o %s" % (config['cxx'], join_flags(config['cxxflags']), i, o))
    return ret

def obj_to_bin(i_files, o_files, config):
    return ["%s %s %s -o %s" % (config['ld'], join_flags(config['ldflags']), ' '.join(i_files), o_files[0])]

def elf_to_bin(i_files, o_files, config):
    return ["%s -O binary %s %s" % (config['objcopy'], i_files[0], o_files[0])]
