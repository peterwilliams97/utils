"""
Flatten a nested directory

Created on 10/10/2010

@author: peter
"""
import os
import fnmatch
import glob 
import shutil

def mk_dir(dir):
    try:
        os.mkdir(dir)
    except:
        pass

def recursive_glob(dir_name, mask):
    path_list = []
    for root, dirs, files in os.walk(dir_name):
        for f in fnmatch.filter(files, mask):
            path_list.append(os.path.join(root, f))
    return path_list
    
def flatten_path(path):
    flat_path = path.replace('\\', '_').replace('/', '_').replace(':', '_')
    clean_path = flat_path.replace(' ', '_').replace('-', '_').replace('&', '_').replace('#', '_').replace('=', '_')
    return clean_path

#print 'os.sep:', os.sep    
def directoryize(path):
    """Make a file path or path fragment end in a slash. Our convention is that each directory
        has trailing slash"""
    if path[-1] != '\\' and path[-1] != '/':
        return path + os.sep    
    return path
    
if __name__ == '__main__':
    import sys
    import optparse

    parser = optparse.OptionParser('usage: python ' + sys.argv[0] + ' <in dir> <mask> <out dir>')
  
    (options, args) = parser.parse_args()
    
    if len(args) < 3:
        print parser.usage
        print 'options:', options
        print 'args:', args
        exit()

    in_dir = directoryize(args[0])
    mask = args[1]
    out_dir = directoryize(args[2])   

    if not os.path.isdir(in_dir):
        print in_dir, 'is not a directory'
        exit()
    
    mk_dir(out_dir)
    if not os.path.isdir(out_dir):
        print out_dir, 'is not a directory'
        exit()        

    if in_dir == out_dir:
        print 'Cannot flatten a directory onto itself'
        exit()        

    print 'in_dir :', in_dir
    print 'mask   :', mask
    print 'out_dir:', out_dir

    # Simple form 
    # for path in recursive_glob(in_dir, mask):
    #   shutil.copyfile(path, os.path.join(out_dir, flatten_path(path[len(in_dir):])))
    
    # The following shows how it works 
    
    in_path_list = recursive_glob(in_dir, mask)
    print len(in_path_list), 'files'
    print '-' * 60
    print '\n'.join('\t%s' % path for path in in_path_list)
    print '-' * 60
    
    flat_path_dict = {}
    for path in in_path_list:
              
        sub_path = path[len(in_dir):]
        flat_path = flatten_path(sub_path)
        out_path = os.path.join(out_dir, flat_path)
                
        print 'path:', path
        print ' sub:', ' ' * len(in_dir) + sub_path
        print ' out:', out_path
        print 'flat:', flat_path
        print '-' * 40
        flat_path_dict[path] = out_path
    
    for i,path in enumerate(sorted(flat_path_dict.keys())):
        out_path = flat_path_dict[path]
        print i, path, '=>', out_path
        shutil.copyfile(path, out_path)
