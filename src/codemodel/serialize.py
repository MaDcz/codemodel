import json
from model import *
import sys


# ==============================================================================
# Serialization
# ==============================================================================


class ModelToDictConvertor(ModelVisitor):

    def __init__(self):
        super(ModelToDictConvertor, self).__init__()

        self._res_dict = None
        self._child_dicts_stack = None
    #enddef

    def result(self):
        return self._res_dict
    #enddef

    def visit_model_node(self, node):
        self._store_result(ModelToDictConvertor._node_to_dict(node))
    #enddef

    def visit_model_block_node(self, node):
        node_dict = ModelToDictConvertor._node_to_dict(node)
        self._store_result(node_dict)

        parent_stack = self._child_dicts_stack
        node_dict["nodes"] = []
        self._child_dicts_stack = node_dict["nodes"]
        try:
            super(ModelToDictConvertor, self).visit_model_block_node(node)
        finally:
            self._child_dicts_stack = parent_stack
    #enddef

    def _store_result(self, node_dict):
        if self._child_dicts_stack is None:
            # started to serialize different model
            self._res_dict = None

        if self._res_dict is None:
            self._res_dict = node_dict
        else:
            self._child_dicts_stack.append(node_dict)
    #enddef

    @staticmethod
    def _node_to_dict(node):
        d = dict()
        d["type"] = ModelToDictConvertor._node_type_to_string(type(node))
        return d
    #enddef

    @staticmethod
    def _node_type_to_string(node_type):
        return "{0}{1}{2}".format(node_type.__module__,
                "." if node_type.__module__ else "", node_type.__name__) 
    #enddef

#endclass


class JsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ModelNode):
            convertor = ModelToDictConvertor()
            o.accept(convertor)
            node_dict = convertor.result()
            assert node_dict is not None
            return node_dict
        else:
            return super(JsonEncoder, self).default(o)
    #enddef

#endclass


def to_json(node):
    # TODO Pretty-printing and minimalistic for IPC.
    return JsonEncoder().encode(node)
#enddef


# ==============================================================================
# Deserialization
# ==============================================================================


class JsonDecoder(json.JSONDecoder):

    def decode(self, s):
        d = super(JsonDecoder, self).decode(s)
        assert isinstance(d, dict)
        return JsonDecoder._node_from_dict(d)
    #enddef

    @staticmethod
    def _node_from_dict(d):
        from pydoc import locate

        def get_mandatory_value(key):
            if key not in d:
                raise RuntimeError("Key '{0}' is missing in the dictionary deserialized from JSON".format(key))
            return d[key]
        #enddef

        node_type_str = get_mandatory_value("type")
        node_type = locate(node_type_str)
        if not node_type:
            raise RuntimeError("Can't locate node type '{0}'".format(node_type_str))
        elif ModelNode not in node_type.mro():
            raise RuntimeError("The node type '{0}' isn't based on '{1}'"
                    .format(node_type_str, ModelToDictConvertor._node_type_to_string(ModelNode)))

        node = node_type()

        if isinstance(node, ModelBlockNode):
            for child_dict in d.get("nodes", []):
                node.add(JsonDecoder._node_from_dict(child_dict))

        return node
    #enddef

#endclass


def from_json(json_str):
    return JsonDecoder().decode(json_str)
#enddef

