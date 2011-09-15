"""
    grep with python regex's
"""
import fnmatch
import glob
import os
import re

def recursive_glob(path_pattern):
    """Like glob except recursese through subdirectories"""
    dir_name, mask = os.path.split(path_pattern)
    path_list = []
    for root, dirs, files in os.walk(dir_name):
        for f in fnmatch.filter(files, mask):
            path_list.append(os.path.join(root, f))
    return path_list

def get_lines(path):
    """Return the contents of file <path> as lines of text"""
    # Would readlines() work better? !@#$
    #bytes = file(path, 'rb').read()
    #line_list = [line.strip() for line in bytes.split('\n')]
    line_list = [line.strip() for line in file(path, 'rb').readlines()]
    return [x for x in line_list if x]

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser('usage: python ' + sys.argv[0] + ' [options] <text pattern> <file pattern>')
    parser.add_option('-i', '--ignore-case', action='store_true', dest='ignore_case', default=False, help='case-insensitive match')
    parser.add_option('-r', '--recursive', action='store_true', dest='recursive', default=False, help='recurse through sub-directories')
    parser.add_option('-l', '--names-only', action='store_true', dest='names_only', default=False, help='show file names only')
    (options, args) = parser.parse_args()

    if len(args) < 2:
        print parser.usage
        print 'options:', options
        print 'args', args
        exit()
    
    # The main parameters    
    text_pattern = args[0]
    path_pattern = args[1]
    re_options = 0
    if  options.ignore_case:
        re_options |= re.IGNORECASE
        
    print 'text_pattern:', text_pattern
    print 'path_pattern:', path_pattern
    print 're_options:', re_options
    
    regex = re.compile(text_pattern, re_options)
    
    if options.recursive:
        path_list = recursive_glob(path_pattern) 
    else:
        path_list = glob.glob(path_pattern)
    
    for i, path in enumerate(path_list):
        line_list = get_lines(path)
        matches = [(j, line) for (j, line) in enumerate(line_list) if regex.search(line)]
        if matches:
            print '%3d: %s' % (i,path)
            if not options.names_only:
                for j, line in matches:
                    print '%9d: %s' % (j, line)
 
    