import json
from model import *
import sys


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
        d["type"] = str(type(node))
        return d
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
