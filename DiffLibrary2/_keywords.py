'''
Copyright 03/01/2014 Jules Barnes

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import sys, os, subprocess
from robot.libraries.BuiltIn import BuiltIn

class keywords(object):

    rootDiffDir = os.path.abspath(os.path.join(__file__, '..'))
    
    def __init__(self):
        self.builtin = BuiltIn()

    def _getdiff(self):
        ''' returns path to diff depending on platform '''

        diff = 'diff --strip-trailing-cr'
        if 'win' in sys.platform:
            diff = "%s --strip-trailing-cr " %os.path.join(self.rootDiffDir, 'bin', 'diff.exe')
        return diff

    def _newdiff(self, actfile, reffile, diff_params=None, diff_func='_getdiff'):
        ''' compare two files

        *actfile:* sxv4dump file created in latest build

        *reffile:* reference sxv4dump file, gzipped

        *diff_cmd:* custom diff command'''

        diff_types = {'_getdiff': self._getdiff}
        diff_lines = {'_getdiff': 2}

        for diffFiles in (actfile, reffile):
            if not os.path.exists(diffFiles):
                self.builtin.fail("%s doesn't exist" %diffFiles)


        # construct the diff command
        diff_function = diff_types.get(diff_func, '_getdiff')
        if diff_params != None:
            diff_cmd = '%s %s "%s" "%s"' %(diff_function(), diff_params, actfile, reffile)
        else:
            diff_cmd = '%s "%s" "%s"' %(diff_function(), actfile, reffile)
        output, rc = self._run(diff_cmd)

        lines = output.splitlines()

        # code 127 shows that shell hasn't found the command
        if rc == 127: 
            self.builtin.fail(output)
        else:
            if diff_func == '_getdiff':
                if rc == 2 or len(lines) == 1: 
                    self.builtin.fail(output)

        # if there is no differences there will still be some lines remaining 
        # because the filter will remove the timestap diff's
        lines_to_skip = diff_lines.get(diff_func, '_getdiff')
        if lines and len(lines) > lines_to_skip:
            print '\n'.join(lines)
            self.builtin.fail("differences found between %s and %s" % (actfile, reffile))



    def diff_files(self, file1, file2, diff_params=None, fail=True):
        ''' Diff two text files

        `file1`: absolute path to the first first file

        `file2`: absolute path to the first second file

        `diff_params`: Parameters that can be passed to the diff program specific to your OS.
        
        `fail`:  If there are differences it will throw an exception and test will fail
                 defaults to True, if False test's will continue '''

        self.builtin.log("file1: %s" %file1)
        self.builtin.log("file2: %s" %file2)

        fail = self.builtin.convert_to_boolean(fail)
        if fail:
            self._newdiff(file1, file2, diff_params)
        else:
            try:
                self._newdiff(file1, file2, diff_params)
            except Exception, e:
                self.builtin.log(e)


    def _run(self, cmd):
        ''' internal run command '''

        if not cmd: return

        self.builtin.log(cmd)
        #cmd = process_cmd(cmd)

        # run the given command in a child shell process (cmd.exe on win and sh/bash on *nix)
        self.cmd = subprocess.Popen(cmd + ' 2>&1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # it will block here and try to read everything into memory
        output = self.cmd.communicate()[0]

        return output, self.cmd.wait()

