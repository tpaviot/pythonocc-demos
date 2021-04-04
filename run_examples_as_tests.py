#!/usr/bin/env python

##Copyright 2009-2019 Thomas Paviot (tpaviot@gmail.com)
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU Lesser General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Lesser General Public License for more details.
##
##You should have received a copy of the GNU Lesser General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

# look for all example names
import os
import glob
import sys
import subprocess
import time

def worker(example_name):
    # += operation is not atomic, so we need to get a lock:
    print("running %s ..." % example_name, end="")
    try:
        subprocess.check_output([sys.executable, example_name],
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
        print("[passed]")
        return True
    except subprocess.CalledProcessError as cpe:
        print("%s" % cpe.output)
        print("[failed]")
        return False

if __name__ == "__main__":
    init_time = time.time()

    # find examplessubdir from current file
    path = os.path.abspath(__file__)
    test_dirname = os.path.dirname(path)
    examples_directory = os.path.join(test_dirname, 'examples')
    os.chdir(examples_directory)
    all_examples_file_names = glob.glob('core_*.py')

    # some tests have to be excluded from the automatic
    # run. For instance, qt based examples
    tests_to_exclude = ['core_display_signal_slots.py',
                        'core_visualization_overpaint_viewer.py'
                        ]

    # remove examples to excludes
    for test_name in tests_to_exclude:
        all_examples_file_names.remove(test_name)

    nbr_examples = len(all_examples_file_names)

    os.environ["PYTHONOCC_OFFSCREEN_RENDERER"] = "1"
    os.environ["PYTHONOCC_OFFSCREEN_RENDERER_DUMP_IMAGE"] = "1"
    os.environ["PYTHONOCC_SHUNT_WEB_SERVER"] = "1"

    # loop over each example
    failed = 0
    for example_file_name in all_examples_file_names:
        test_result = worker(example_file_name)
        if not test_result:
            failed += 1

    print("Test examples results :")
    print("\t %i/%i tests passed" % ((nbr_examples - failed), nbr_examples))

    if failed > 0:
        print("%i tests failed" % failed)

    print("Total time to run all examples: %fs" %(time.time() - init_time))

    # if failed, exit with error
    if failed > 0:
        sys.exit(1)
