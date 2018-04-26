from functools import wraps


class HandledNodeWrapper(object):

    def __init__(self, node):
        super(HandledNodeWrapper, self).__init__()
        self.node = node
    #enddef

#endclass


class ModelVisitor(object):

    def __init__(self):
        super(ModelVisitor, self).__init__()
    #enddef

    def visit_model_node(self, node):
        pass
    #enddef

    def visit_model_block_node(self, node):
        node = ModelNode.unwrap(node)
        for n in node.nodes:
            n.accept(self)
    #enddef

#endclass


def model_visitor_accept(method):
    @wraps(method)
    def wrapper(self, visitor):
        if isinstance(visitor, ModelVisitor):
            method(self, visitor)
        else:
            raise TypeError, "Invalid visitor type (expected %s, have %s)" \
                    % (str(Visitor), str(type(visitor)))
    #enddef
    return wrapper
#enddef


class ModelNode(object):

    def __init__(self, data=dict()):
        super(ModelNode, self).__init__()

        self.data = data
        self.data["type"] = str(type(self))
    #enddef

    def data_dict(self):
        return self.data
    #enddef

    @model_visitor_accept
    def accept(self, visitor):
        visitor.visit_model_node(self)
    #enddef

    @staticmethod
    def mark_as_handled(node):
        if not isinstance(node, ModelNode):
            raise TypeError, "Node is not a ModelNode instance (%s)" % str(type(node))
        return HandledNodeWrapper(node)
    #enddef

    @staticmethod
    def was_handled(node):
        if isinstance(node, HandledNodeWrapper):
            return True
        else:
            return False
    #enddef

    @staticmethod
    def unwrap(node):
        if isinstance(node, HandledNodeWrapper):
            return node.node
        elif isinstance(node, ModelNode):
            return node
        else:
            raise TypeError, "Not a ModelNode instance"
    #enddef

#endclass


class ModelBlockNode(ModelNode):

    def __init__(self):
        super(ModelBlockNode, self).__init__()
        self.nodes = []
    #enddef

    def add(self, node):
        if not isinstance(node, ModelNode):
            raise TypeError, "Added node isn't a ModelNode instance"
        self.nodes.append(node)
        return self
    #enddef

    @model_visitor_accept
    def accept(self, visitor):
        visitor.visit_model_block_node(self)
    #enddef

#endclass
