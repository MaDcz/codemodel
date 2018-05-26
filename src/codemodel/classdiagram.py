from __future__ import absolute_import

from .model import *


def class_diagram_visitor_accept(method):
    @wraps(method)
    def wrapper(self, visitor):
        if isinstance(visitor, ClassDiagramVisitor):
            method(self, visitor)
        else:
            super(type(self), self).accept(visitor)
    #enddef
    return wrapper
#enddef


class Package(ModelBlockNode):

    # TODO For the purpose of deserialization the constructor can't take any custom
    # arguments. The members will be done through properties either.
    #def __init__(self, name):
    #    super(Package, self).__init__()
    #    self.name = name
    ##enddef

    @class_diagram_visitor_accept
    def accept(self, visitor):
        visitor.visit_package(self)
    #enddef

#endclass


class Class(ModelBlockNode):

    # TODO For the purpose of deserialization the constructor can't take any custom
    # arguments. The members will be done through properties either.
    #def __init__(self, name):
    #    super(Class, self).__init__()
    #    self.name = name
    ##enddef

    @class_diagram_visitor_accept
    def accept(self, visitor):
        visitor.visit_class(self)
    #enddef

#endclass


class Attribute(ModelNode):

    # TODO For the purpose of deserialization the constructor can't take any custom
    # arguments. The members will be done through properties either.
    #def __init__(self, name, type):
    #    super(Attribute, self).__init__()
    #    self.name = name
    #    self.type = type
    ##enddef

    @class_diagram_visitor_accept
    def accept(self, visitor):
        visitor.visit_attribute(self)
    #enddef

#endclass


class Operation(ModelNode):

    def __init__(self):
        super(Operation, self).__init__()
    #enddef

    @class_diagram_visitor_accept
    def accept(self, visitor):
        visitor.visit_operation(self)
    #enddef

#endclass


class Enum(ModelNode):

    def __init__(self):
        super(Enum, self).__init__()
    #enddef

    @class_diagram_visitor_accept
    def accept(self, visitor):
        visitor.visit_enum(self)
    #enddef

#endclass


class Artifact(ModelNode):

    def __init__(self):
        super(Artifact, self).__init__()
    #enddef

    @class_diagram_visitor_accept
    def accept(self, visitor):
        visitor.visit_artifact(self)
    #enddef

#endclass


def class_diagram_node_visit(method):
    @wraps(method)
    def wrapper(self, node_or_wrapper):
        def get_method_impl(name, node_or_wrapper=node_or_wrapper):
            '''Tries to determine if the decorated method is overriden and if so, it returns
               base class implementation of method given by the passed name. Otherwise it
               uses a standarm (polymorphic) resolution to get the method instance.'''
            method_impl = None # picked method implementation
            if ModelNode.was_handled(node_or_wrapper):
                method_impl = getattr(super(ClassDiagramVisitor, self), name)
            elif getattr(self.__class__, method.__name__).__module__ != __name__:
                node_or_wrapper = ModelNode.mark_as_handled(node_or_wrapper)
                method_impl = getattr(super(ClassDiagramVisitor, self), name)
            else:
                method_impl = getattr(self, name)
            return (method_impl, node_or_wrapper)
        #enddef
        method_impl = None
        node = ModelNode.unwrap(node_or_wrapper)
        if isinstance(node, ModelBlockNode):
            method_impl, node_or_wrapper = get_method_impl("visit_model_block_node")
        elif isinstance(node, ModelNode):
            method_impl, node_or_wrapper = get_method_impl("visit_model_node")

        if method_impl is None:
            raise TypeError("Unknown node type")
        else:
            method_impl(node_or_wrapper)
    #enddef
    return wrapper
#enddef


class ClassDiagramVisitor(ModelVisitor):

    def __init__(self):
        super(ClassDiagramVisitor, self).__init__()
    #enddef

    @class_diagram_node_visit
    def visit_package(self, node):
        pass
    #enddef

    @class_diagram_node_visit
    def visit_class(self, node):
        pass
    #enddef

    @class_diagram_node_visit
    def visit_attribute(self, node):
        pass
    #enddef

    @class_diagram_node_visit
    def visit_operation(self, node):
        pass
    #enddef

    @class_diagram_node_visit
    def visit_enum(self, node):
        pass
    #enddef

    @class_diagram_node_visit
    def visit_artifact(self, node):
        pass
    #enddef

#endclass
