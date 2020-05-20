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

import sys
import os
import imp
import subprocess

import lib.build

root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))

verbosity = 0

__nodes__ = dict()

def dict_override(base, over):
    ret = dict(base)
    for k,v in over.iteritems():
        ret[k] = v
    return ret

def debug_v(v, msg, nl=True):
    '''Prints a debug message with the given verbosity.

    @param v The verbosity of the debug message
    @param msg The debug message
    @param nl Whether or not to append '\\n'
    '''
    if(v <= verbosity):
        sys.stderr.write(msg + ('\n' if nl else ''))

def fail(msg, nl=True):
    '''Fails out with a message at 0 verbosity.

    @param msg The failure message
    @param nl Whether or not to append '\\n'
    '''
    debug_v(0, msg, nl)
    exit(1)

def get_path(suffix, root):
    '''Returns the path for the directory under the given root directory.

    @param suffix The relative path from the root
    @param root The root directory (defaults to the Unibed root directory)

    @return The full path
    @throws Exception if the resulting path does not exist
    '''
    ret = os.path.join(root, suffix)

    if not os.path.isdir(ret):
        raise Exception("Path '%s' does not exist" % ret)

    return ret

def get_entries(suffix, root):
    '''Gets the entries for the directory produced by get_path(suffix, root).

    @param suffix The relative path from the root
    @param root The root directory (defaults to the Unibed root directory)

    @return The full path
    @throws Exception if the resulting path does not exist
    '''
    path = get_path(suffix, root)
    entries = os.listdir(path)
    entries = filter(lambda entry : os.path.isdir(os.path.join(path, entry)),
                     entries)
    return entries

class UnibedNode(object):

    @staticmethod
    def getNode(path):
        # If this node has already been constructed, just use that
        if path in __nodes__.keys():
            return __nodes__[path]

        return UnibedNode(path)

    def __init__(self, path):
        '''Constructs a UnibedNode for the given path. All directories in Unibed
        constitute build units, and are treated as nodes in a build graph. Every
        directory is required to contain a config.py that describes the
        properties of that node. These properties are added to the UnibedNode
        constructed for that directory.

        @param path The path of the directory for this UnibedNode
        '''
        self.path = path

        # If this node does not correspond to the root path, build a node for
        # the parent directory, and assign it to the parent property.
        if not path == root_path:
            self.parent = UnibedNode.getNode(
                os.path.abspath(os.path.join(path, '..')))
        else:
            self.parent = None

        # Load the config.
        self.config_path = os.path.abspath(os.path.join(path, 'config.py'))

        if not os.path.exists(self.config_path):
            fail('config.py does not exist in %s' % path)

        raw_module_name = 'config_%d' % len(__nodes__)

        # Build a list of all of the parents of this node up to the root.
        testnode = self
        rwalknodes = []
        while(testnode):
            rwalknodes.append(testnode)
            testnode = testnode.parent

        # Build a fresh module and add the node path to it.
        self.raw_config = imp.new_module(raw_module_name)
        sys.modules[raw_module_name] = self.raw_config

        # Walk the parents list in reverse and import the configs on top of each
        # other.
        for testnode in rwalknodes[::-1]:
            self.raw_config.node = testnode
            self.raw_config = imp.load_source(raw_module_name, testnode.config_path)


        #self.raw_config = imp.load_source(raw_module_name, self.config_path)

        self.config = dict(filter(lambda kv : not kv[0][:2] == '__',
                                  vars(self.raw_config).iteritems()))

        # This path's config overrides the parent's config.
        if self.parent:
            self.config = dict_override(self.parent.config, self.config)

        __nodes__[path] = self

        self.path = path
        self.name = os.path.basename(self.path)

    def makeAbsPath(self, path):
        return os.path.abspath(os.path.join(self.path, path))

    def makeAbsPaths(self, paths):
        return map(self.makeAbsPath, paths)

def config_hasitem(config, item):
    return vars(config).has_key(item)

def build(app, board):
    '''Builds an app for a board.
    '''
    build_dict = dict_override(board.config, app.config)

    root_fns = lib.build.FileNamespace.root()

    for node in (board, app):
        if(config_hasitem(node.raw_config, "files")):
            root_fns.addFiles(node.makeAbsPaths(node.raw_config.files))
        if(config_hasitem(node.raw_config, "files_regex")):
            root_fns.addFiles(lib.build.findFiles(node.path,
                                                  node.raw_config.files_regex,
                                                  True))

    compiled_steps = []

    for step in board.raw_config.build_steps:
        in_filesets, out_filesets, step_f = lib.build.process_step(step,
                                                                   root_fns)

        parallel_steps = []

        for in_files, out_files in zip(in_filesets, out_filesets):
            parallel_steps.extend(step_f(in_files, out_files, build_dict))

        compiled_steps.append(parallel_steps)

    for step in compiled_steps:
        for command in step:
            debug_v(1, command)
            subprocess.call(command.split(' '))
