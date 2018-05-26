#!/usr/bin/python

from functools import wraps

import codemodel


def cpp_model_visitor_accept(method):
    @wraps(method)
    def wrapper(self, visitor):
        if isinstance(visitor, CppModelVisitor):
            method(self, visitor)
        else:
            super(type(self), self).accept(visitor)
    #enddef
    return wrapper
#enddef

class Namespace(codemodel.Package):

    def __init__(self, name):
        super(Namespace, self).__init__()

        if not name:
            raise ValueError("No name given for namespace")

        self.name = name
    #enddef

    @cpp_model_visitor_accept
    def accept(self, visitor):
        visitor.visit_cpp_namespace(self)
    #enddef

#endclass

class Class(codemodel.Class):

    def __init__(self, name, struct=False):
        super(Class, self).__init__()

        if not name:
            raise ValueError("No name given for class")

        self.name = name
        self.struct = struct
    #enddef

    @cpp_model_visitor_accept
    def accept(self, visitor):
        visitor.visit_cpp_class(self)
    #enddef

#endclass

class Method(codemodel.Operation):

    def __init__(self, name, retval=None, params=[], static=False):
        super(Method, self).__init__()

        if not name:
            raise ValueError("No name given for method")
        if retval is not None and not retval:
            raise ValueError("Return value cannot be empty")
        elif not retval:
            retval = "void"

        self.name = name
        self.retval = retval
        self.params = params
        self.static = static
    #enddef

    @cpp_model_visitor_accept
    def accept(self, visitor):
        visitor.visit_cpp_method(self)
    #enddef

#endclass


def cpp_model_node_visit(method):
    @wraps(method)
    def wrapper(self, node_or_wrapper):
        def get_method_impl(name, node_or_wrapper=node_or_wrapper):
            '''Tries to determine if the decorated method is overriden and if so, it returns
               base class implementation of method given by the passed name. Otherwise it
               uses a standarm (polymorphic) resolution to get the method instance.'''
            method_impl = None # picked method implementation
            if codemodel.ModelNode.was_handled(node_or_wrapper):
                method_impl = getattr(super(CppModelVisitor, self), name)
            elif getattr(self.__class__, method.__name__).__module__ != __name__:
                node_or_wrapper = codemodel.ModelNode.mark_as_handled(node_or_wrapper)
                method_impl = getattr(super(CppModelVisitor, self), name)
            else:
                method_impl = getattr(self, name)
            return (method_impl, node_or_wrapper)
        #enddef

        # pick the right method according to a node type
        method_impl = None
        node = codemodel.ModelNode.unwrap(node_or_wrapper)
        if isinstance(node, codemodel.Package):
            method_impl, node_or_wrapper = get_method_impl("visit_package")
        elif isinstance(node, codemodel.Class):
            method_impl, node_or_wrapper = get_method_impl("visit_class")
        elif isinstance(node, codemodel.Attribute):
            method_impl, node_or_wrapper = get_method_impl("visit_attribute")
        elif isinstance(node, codemodel.Operation):
            method_impl, node_or_wrapper = get_method_impl("visit_operation")
        elif isinstance(node, codemodel.Enum):
            method_impl, node_or_wrapper = get_method_impl("visit_enum")
        elif isinstance(node, codemodel.Artifact):
            method_impl, node_or_wrapper = get_method_impl("visit_artifact")

        if method_impl is None:
            raise TypeError("Unknown node type")
        else:
            method_impl(node_or_wrapper)
    #enddef
    return wrapper
#enddef

class CppModelVisitor(codemodel.ClassDiagramVisitor):

    def __init__(self):
        super(CppModelVisitor, self).__init__()
    #enddef

    @cpp_model_node_visit
    def visit_cpp_namespace(self, node):
        pass
    #enddef

    @cpp_model_node_visit
    def visit_cpp_class(self, node):
        pass
    #enddef

    @cpp_model_node_visit
    def visit_cpp_method(self, node):
        pass
    #enddef

#endclass

