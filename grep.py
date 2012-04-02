"""
    A grep that behaves the way that I want (which may not be to everyone's liking).
    "Improvements" over regular grep:
    - Uses python regex's
    - Applies file masks in recursion
    NOTE: Not fully featured.
    Should work with Python 2.x  for x >= 5
"""
import fnmatch
import glob
import os
import re
import sys

def _recursive_glob(path_pattern):
    """Like glob() except recurses through subdirectories"""
   
    dir_name, mask = os.path.split(path_pattern)
    if not dir_name:
        dir_name = '.'
    print '_recursive_glob(%s) dir_name=%s, mask=%s' % (path_pattern, dir_name, mask)
    print '-' * 80
    for root, dirs, files in os.walk(dir_name):
        for filename in fnmatch.filter(files, mask):
            full_path = os.path.join(root,filename)
            if not os.path.isdir(full_path):
                yield(full_path)

def _get_matches_for_file(f, is_match, max_lines):
    """Return list of (line number, lines) matching function <is_match> for lines in
        file <f>. NOTE: line number is 1-offset
    """
    # Implementation asssumes file object is implemented as a generator of lines
    for j, line in enumerate(f):
        if max_lines >= 0 and j >= max_lines:
            break
        if is_match(line):
            yield j+1, line.rstrip('\n').rstrip('\r')

def _get_matches_for_path(path, is_match, max_lines):
    """Return list of (line number, lines) matching function <is_match> for lines in
        file named <path>.
    """
    try:
        f = open(path, 'rb')
    except IOError:
        print '%s: Could not open' % path    

    for j, line in _get_matches_for_file(f, is_match, max_lines):
        yield j, line

def show_matches(text_pattern, path_pattern, re_options, recursive, names_only, counts, invert_match, 
                max_lines):
    """Show matches of regular expression given by <text_pattern> and regex options <re_options>
        in files matched by <path_pattern>.
        If not <path_pattern> then read from stdin.
        If <recursive> then recurse search through sub-directories.
        If <names_only> then show only file names and not lines.
        If <counts> then show file names and line counts.
        If <invert_match> then show files that don't match.
"""
    regex = re.compile(text_pattern, re_options)
    is_match = lambda x: regex.search(x) is not None
    
    if invert_match:
        names_only = True
   
    print 'text_pattern=%s' % text_pattern
    print 'text_pattern=%s' % path_pattern
    print 'recursive=%s' % recursive
    print '-' * 80

    if not path_pattern:
        # stdin case
        for _, line in _get_matches_for_file(sys.stdin, is_match, max_lines):
            print line
    else:
        # file pattern cases
        if recursive:
            path_list = _recursive_glob(path_pattern)  
        else: 
            path_list = [p for p in glob.glob(path_pattern) if not os.path.isdir(p)]

        for path in path_list:
            if names_only:
                if bool(any(_get_matches_for_path(path, is_match, max_lines))) != invert_match:
                    print path
            elif counts:
                print '%s:%d' % (path, len([x for x in _get_matches_for_path(path, is_match, max_lines)]))
            else:
                for j, line in _get_matches_for_path(path, is_match, max_lines):
                    print '%s:%d:%s' % (path, j, line)

if __name__ == '__main__':
    import optparse

    parser = optparse.OptionParser('python ' + sys.argv[0] + ' [options] <text pattern> [<file pattern>]')
    parser.add_option('-i', '--ignore-case', action='store_true', dest='ignore_case', default=False, help='case-insensitive match')
    parser.add_option('-r', '--recursive', action='store_true', dest='recursive', default=False, help='recurse through sub-directories')
    parser.add_option('-l', '--names-only', action='store_true', dest='names_only', default=False, help='print file names only')
    parser.add_option('-c', '--count', action='store_true', dest='counts', default=False, help='print only a count of matching lines per FILE')
    parser.add_option('-v', '--invert-match', action='store_true', dest='invert_match', default=False, help='print files that do not match')
    parser.add_option('-m', '--max-lines', dest='max_lines', default='-1', help='maximum number of lines to search in each file')
    (options, args) = parser.parse_args()

    if len(args) < 1:
        print parser.usage
        print '--help for more information'
        exit()
 
    text_pattern = args[0]
    path_patttern = args[1] if len(args) >= 2 else None

    # re_options is built from command line flags
    re_options = 0
    if options.ignore_case:
        re_options |= re.IGNORECASE

    show_matches(text_pattern, path_patttern, re_options, options.recursive, options.names_only,
        options.counts, options.invert_match, int(options.max_lines))
        