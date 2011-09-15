"""
    A grep that behaves the way that I want (which may not be to everyone's liking)
    
    "Improvements" over regular grep:
        - Uses python regex's
        - Applies file masks in recursion
        
    NOTE: Not fully featured
"""
import fnmatch
import glob
import os
import re

def recursive_glob(path_pattern):
    """Like glob except recurse through subdirectories"""
    dir_name, mask = os.path.split(path_pattern)
    path_list = []
    for root, dirs, files in os.walk(dir_name):
        for f in fnmatch.filter(files, mask):
            path_list.append(os.path.join(root, f))
    return path_list

def get_matches(path, regex, is_match):
    """Return list of (line number, lines) matching compile regular expression <regex> and matching 
        function <is_match> for lines in file named <path>"""
    with open(path, 'rt') as f:
        return [(j,line) for (j,line) in enumerate(f.readline()) if is_match(line)]
    
def show_matches(path_list, text_pattern, re_options, names_only, invert_match):
    """Show matches of regular expression given by <text_pattern> and regex options <re_options>
        in files with names in <path_list>. 
        If <names_only> then only show file names and not linea
        If <invert_match> then show files that don't match."""
        
    regex = re.compile(text_pattern, re_options)
    
    if invert_match:
        def is_match(line):
            return regex.search(line) is None
    else:
        def is_match(line):
            return regex.search(line) is not None
    
    for i, path in enumerate(path_list):
        matches = get_matches(path, regex, is_match)
        if matches:
            print '%3d: %s' % (i,path)
                if not names_only:
                    for j, line in matches:
                        print '%9d: %s' % (j, line)    
     
_VERBOSE = True
     
if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser('usage: python ' + sys.argv[0] + ' [options] <text pattern> <file pattern>')
    parser.add_option('-i', '--ignore-case', action='store_true', dest='ignore_case', default=False, help='case-insensitive match')
    parser.add_option('-r', '--recursive', action='store_true', dest='recursive', default=False, help='recurse through sub-directories')
    parser.add_option('-l', '--names-only', action='store_true', dest='names_only', default=False, help='show file names only')
    parser.add_option('-y', '--invert-match', action='store_true', dest='invert_match', default=False, help='show files/lines that do not match')
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
    
    if _VERBOSE:
        print 'text_pattern:', text_pattern
        print 'path_pattern:', path_pattern
        print 're_options:', re_options
        print 'names_only:', options.names_only
        print 'invert match:', option.invert_match
    
    if options.recursive:
        path_list = recursive_glob(path_pattern) 
    else:
        path_list = glob.glob(path_pattern)

    show_matches(path_list, text_pattern, re_options, options.names_only, options.invert_match)
 
