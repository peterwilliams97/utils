"""
    A grep that behaves the way that I want (which may not be to everyone's liking).
    
    "Improvements" over regular grep:
        - Uses python regex's
        - Applies file masks in recursion
        
    NOTE: Not fully featured
"""
import fnmatch
import glob
import os
import re

def _recursive_glob(path_pattern):
    """Like glob() except recurses through subdirectories"""
    dir_name, mask = os.path.split(path_pattern)
    for root, dirs, files in os.walk(dir_name):
        for filename in fnmatch.filter(files, mask):
            yield(os.path.join(root,filename))

def _get_matches(path, is_match):
    """Return list of (line number, lines) matching function <is_match> for lines in 
        file named <path>.
    """
    # Implementation asssumes open() is implemented as a generator of lines
    with open(path, 'rb') as f:
        for j, line in enumerate(f):
            if is_match(line):
                yield j, line.rstrip('\n')

def show_matches(text_pattern, path_pattern, re_options, recursive, names_only, invert_match):
    """Show matches of regular expression given by <text_pattern> and regex options <re_options>
        in files matched by <path_pattern>.
        If <recursive> then recurse search through sub-directories.
        If <names_only> then only show file names and not lines.
        If <invert_match> then show files that don't match.
    """
    path_list = _recursive_glob(path_pattern) if recursive else glob.glob(path_pattern)
    regex = re.compile(text_pattern, re_options)
    is_match = lambda x: (regex.search(x) is not None) != invert_match

    for path in path_list:
        if names_only:
            if any(_get_matches(path, is_match)):
                print path
        else:
            for j, line in _get_matches(path, is_match):
                print '%s:%d:%s' % (path, j, line) 

if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser('python ' + sys.argv[0] + ' [options] <text pattern> <file pattern>')
    parser.add_option('-i', '--ignore-case', action='store_true', dest='ignore_case', default=False, help='case-insensitive match')
    parser.add_option('-r', '--recursive', action='store_true', dest='recursive', default=False, help='recurse through sub-directories')
    parser.add_option('-l', '--names-only', action='store_true', dest='names_only', default=False, help='show file names only')
    parser.add_option('-y', '--invert-match', action='store_true', dest='invert_match', default=False, help='show files/lines that do not match')
    (options, args) = parser.parse_args()

    if len(args) < 2:
        print parser.usage
        print '--help for more information'
        exit()

    # re_options is built from command line flags
    re_options = 0
    if options.ignore_case:
        re_options |= re.IGNORECASE

    show_matches(args[0], args[1], re_options, options.recursive, options.names_only, options.invert_match)