# -*- coding: utf-8 -*-
from __future__ import division
"""
    A grep that behaves the way that I want (which may not be to everyone's liking).
    "Improvements" over regular grep:
    - Uses python regex's
    - Applies file masks in recursion
    NOTE: Not fully featured.
    Should work with Python 2.x  for x >= 5
"""
import glob 
import os
import re
import sys
import utils

def _get_matches_for_file(f, is_match, max_lines):
    """Return list of (line number, lines) matching function <is_match> for lines in
        file <f>. NOTE: line number is 1-offset
    """
    # Implementation assumes file object is implemented as a generator of lines
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
        with open(path, 'rb') as f:
            for j, line in _get_matches_for_file(f, is_match, max_lines):
                yield j, line
    except IOError, e:
        print >> sys.stderr, 'Could not open "%s"' % path, e  

def show_matches(text_pattern, path_pattern, re_options, recursive, names_only, counts, invert_match, 
                suppress_prefix, max_lines, match_only):
    """Show matches of regular expression given by <text_pattern> and regex options <re_options>
        in files matched by <path_pattern>.
        If not <path_pattern> then read from stdin.
        If <recursive> then recurse search through sub-directories.
        If <names_only> then show only file names and not lines.
        If <counts> then show file names and line counts.
        If <invert_match> then show files that don't match.
        If <suppress_prefix> then don't show line numbers and file names.
        If <match_only> then show only contents of match, not whole line.
"""
    regex = re.compile(text_pattern, re_options)
    is_match = lambda x: regex.search(x) is not None
    
    unique_matches = {}
    
    if invert_match:
        names_only = True
        
    if match_only:
        # Store the unique matches
        # Return the matches in case we ever decide to print them as they are found
        def get_match(line, unique_matches): 
            matches = [m.group(0) for m in regex.finditer(line)]
            for s in matches:
                unique_matches[s] = unique_matches.get(s,0) + 1    
            return ', '.join(matches)
        def output(s): pass    
    else:
        # Print whole line that contains match
        def get_match(line, unique_matches): return line
        def output(s): print s  
   
    if not path_pattern:
        # stdin case
        for _, line in _get_matches_for_file(sys.stdin, is_match, max_lines):
            output(get_match(line))
    else:
        # file pattern cases
        for path in utils.glob(path_pattern, recursive=recursive):
            if names_only:
                if bool(any(_get_matches_for_path(path, is_match, max_lines))) != invert_match:
                    output(path)
            elif counts:
                print '%s:%d' % (path, len([x for x in _get_matches_for_path(path, is_match, max_lines)]))
            else:
                if suppress_prefix:
                    for _,line in _get_matches_for_path(path, is_match, max_lines):
                        output(get_match(line))
                else:        
                    for j, line in _get_matches_for_path(path, is_match, max_lines):
                        output('%s:%d:%s' % (path, j, get_match(line, unique_matches)))

    if match_only:
        print '-' * 80
        print 'unique_matches'
        print unique_matches

if __name__ == '__main__':
    import optparse

    parser = optparse.OptionParser('python ' + sys.argv[0] + ' [options] <text pattern> [<file pattern>]')
    parser.add_option('-i', '--ignore-case', action='store_true', dest='ignore_case', default=False, help='case-insensitive match')
    parser.add_option('-r', '--recursive', action='store_true', dest='recursive', default=False, help='recurse through sub-directories')
    parser.add_option('-l', '--names-only', action='store_true', dest='names_only', default=False, help='print file names only')
    parser.add_option('-c', '--count', action='store_true', dest='counts', default=False, help='print only a count of matching lines per FILE')
    parser.add_option('-v', '--invert-match', action='store_true', dest='invert_match', default=False, help='print files that do not match')
    parser.add_option('-o', '--match-only', action='store_true', dest='match_only', default=False, help='show only regex match, not whole line')
    parser.add_option('-s', '--suppress-line-numbers', action='store_true', dest='suppress_prefix', default=False, help='suppress line number and file name prefixes')
    parser.add_option('-m', '--max-lines', dest='max_lines', default='-1', help='maximum number of lines to search in each file')
    (options, args) = parser.parse_args()

    if len(args) < 1:
        print parser.usage
        print '--help for more information'
        sys.exit()
 
    text_pattern = args[0]
    path_patttern = args[1] if len(args) >= 2 else None

    # re_options is built from command line flags
    re_options = 0
    if options.ignore_case:
        re_options |= re.IGNORECASE

    show_matches(text_pattern, path_patttern, re_options, options.recursive, options.names_only,
        options.counts, options.invert_match, options.suppress_prefix, int(options.max_lines), 
        options.match_only)
        