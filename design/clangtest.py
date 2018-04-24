#!/usr/bin/python

class Options(object):
    pass

opts = Options()
opts.showIDs = True
opts.maxDepth = None

def get_cursor_id(cursor, cursor_list = []):
    if not opts.showIDs:
        return None

    if cursor is None:
        return None

    # FIXME: This is really slow. It would be nice if the index API exposed
    # something that let us hash cursors.
    for i,c in enumerate(cursor_list):
        if cursor == c:
            return i

    cursor_list.append(cursor)
    return len(cursor_list) - 1
#enddef


def get_info(node, depth = 0):
    if opts.maxDepth is not None and depth >= opts.maxDepth:
        children = None
    else:
        children = [ get_info(c, depth + 1) for c in node.get_children() ]

    return { 'id' : get_cursor_id(node),
             'kind' : node.kind,
             'usr' : node.get_usr(),
             'spelling' : node.spelling,
             'location' : node.location,
             'extent.start' : node.extent.start,
             'extent.end' : node.extent.end,
             'is_definition' : node.is_definition(),
             'definition id' : get_cursor_id(node.get_definition()),
             'children' : children }
#enddef


def main():
    import clang.cindex
    from pprint import pprint
    import sys

    if len(sys.argv) < 2:
        raise Exception, "Invalid number of arguments. A C++ source file has to be specified."

    clang.cindex.Config.set_library_file('/usr/lib64/libclang.so')

    idx = clang.cindex.Index.create()
    tu = idx.parse(sys.argv[1], [ '-x', 'c++', '-std=c++11', '-nostdinc++' ])
    if not tu:
        raise RuntimeError, "Unable to load input C++ file."

    pprint(('nodes', get_info(tu.cursor, 1)))
#enddef


if __name__ == '__main__':
    main()
#endif
