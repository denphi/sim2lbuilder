import warnings
import importlib
import simtool
from IPython.display import display
from traitlets import Dict, validate, Unicode
from ipywidgets import HBox, Label
import ipysheet

class WidgetConstructor():
    def __init__(self, layx=None):
        self.inputs = {}
        self.outputs = {}
        self.layout = None
        for item, value in layx.items():
            if item == "inputs":
                self.buildParameters(value, self.inputs)  
            elif item == "outputs":
                self.buildParameters(value, self.outputs)  
            elif item == "layout":
                self.layout = self.buildLayout(value)  
            else:
               pass;#warnings.warn(item + " is ignored")  
            
    def buildParameters(self, outputs, storage):
        for item, value in outputs.items():
            if type(value) == dict:
                type_ = ""
                module_ = "ipywidgets"
                params_ = {}
                click_ = None
                if type(value) is dict and value.get("module", None) is None and value.get("layout", None) is None:
                    value["layout"] = {'width' : 'auto'}
                if type(value) is dict and value.get("module", None) is None and value.get("style", None) is None:
                    value["style"] = {'description_width' : 'initial'}
                for item2, value2 in value.items():
                    if item2 == "type":
                        type_ = value2;
                    elif item2 == "click":
                        click_ = value2;
                    elif item2 == "module":
                        module_ = value2;
                    else:
                        params_[item2] = value2
                module = importlib.import_module(module_)
                class_ = getattr(module, type_)
                storage[item] = class_(**params_)   
                self.setClick(storage[item], click_)                
            else:
               warnings.warn(item + " is not a valid description")  


    def buildLayout(self, layout):
        type_ = ""
        module_ = "ipywidgets"
        params_ = {}
        children_ = []
        titles_ = []
        click_ = None
        for item, value in layout.items():
            if item == "type":
                type_ = value;
            elif item == "module":
                module_ = value;
            elif item == "click":
                click_ = value;                
            elif item == "titles":
                titles_ = value
            elif item == "children":
                if type(value) == dict:
                    for item2, value2 in value.items():
                        child_ = None
                        if value2 == None:
                            if (item2 in self.inputs):
                                child_ = self.inputs[item2]
                            elif (item2 in self.outputs):
                                child_ = self.outputs[item2]
                            else :
                               warnings.warn(item2 + " is not a valid element")
                        else:
                            child_ = self.buildLayout(value2)
                        if child_ is not None:
                            children_.append(child_)
                else:
                   warnings.warn(item + " is not a valid description")

            else:
                params_[item] = value
        if (len(titles_) > 0 ):
            params_["titles"] = titles_
        if (len(children_) > 0 ):
            params_["children"] = children_
        module = importlib.import_module(module_)
        class_ = getattr(module, type_)
        instance_ =  class_(**params_) 
        self.setClick(instance_, click_)
        
        for i, title in enumerate(titles_):
            try:
                instance_.set_title(i, title)
            except:
               warnings.warn(title + " can not be assigned")

        return instance_
         
    def setClick(self, instance, function_name):
        if function_name is not None:
            instance.on_click(None, remove=True)
            instance.on_click(lambda a, b=self, c=function_name: getattr(b, c)(b))
               
        
    def display(self):
        display(self.layout)

def simtool_constructor(self, node):
    values = node.value.split(" ", 2)
    tool = values[0]
    path = ""
    action = "values"
    if len(values) > 1:
        path = values[1]
    if len(values) > 2:
        action = values[2]        
    stl = simtool.searchForSimTool(tool)
    if (stl['notebookPath'] == None):
        raise "Simtool is not valid"
    inputs = simtool.getSimToolInputs(stl)
    outputs = simtool.getSimToolOutputs(stl)
    res = {'inputs':{},'outputs':{}}
    for i in inputs:
        res['inputs'][i] = {}
        for j in inputs[i]:
            if inputs[i][j] is None:
                pass;
            elif j == "type":
                if inputs[i][j] == "Integer":
                    res['inputs'][i][j] = "BoundedIntText"
                elif inputs[i][j] == "Number":
                    res['inputs'][i][j] = "BoundedFloatText"
                elif inputs[i][j] == "Boolean":
                    res['inputs'][i][j] = "ToggleButton"
                elif inputs[i][j] == "List":
                    res['inputs'][i][j] = "SelectMultiple"
                    res['inputs'][i]["options"] = inputs[i]["value"]
                elif inputs[i][j] == "Dict":
                    res['inputs'][i][j] = "DictSheet"
                    res['inputs'][i]["module"] = "sim2lbuilder"
                #elif inputs[i][j] == "List":
                #    res['inputs'][i][j] = "TagsInput"
                else:
                    res['inputs'][i][j] = "Text"
            elif j == "desc":                 
                res['inputs'][i]["description"] = inputs[i][j]
            else :
                res['inputs'][i][j] = inputs[i][j]
            
    for i in outputs:
        res['outputs'][i] = {}
        for j in outputs[i]:
            if j == "type":
                res['outputs'][i][j] = "Output"
            else:
                res['outputs'][i][j] = outputs[i][j]
    for subpath in path.split("."):
        res = res.get(subpath, {})
    if action == "keys":
        return {k:None for k in res.keys()}
    else :
        return res
    


class DictSheet(HBox):
    value = Dict({}).tag(sync=True)
    description = Unicode("").tag(sync=True)
    def __init__(self, **kwargs):
        self._table = ipysheet.sheet(columns = 2, row_headers = False, column_headers = ["key", "value"])
        self._label = Label(kwargs.get("description", ""))
        self.cells = []
        self.updating = False
        self.value = kwargs.get("value", {})
        kwargs["children"] = [self._label, self._table]
        HBox.__init__(self, **kwargs);
   
    def _handle_change(self, change):
        table = [[0,0] for i in range(self._table.rows)]
        for cell in self._table.cells:
            table[cell.row_start][cell.column_start] = cell.value
        self.updating = True
        self.value= {i[0]:i[1] for i in table}
        self.updating = False

        
    @validate('value')
    def _valid_value(self, proposal):
        if isinstance(proposal['value'], dict):
            if self.updating is False:
                self._table.rows = len(proposal['value'].keys())
                i=0
                for k,v in proposal['value'].items():
                    if i >= len(self.cells):
                        cell_0 = ipysheet.cell(i, 0, value=k)
                        cell_0.observe(lambda c, s=self: s._handle_change(c), "value")
                        cell_1 = ipysheet.cell(i, 1, value=v)
                        cell_1.observe(lambda c, s=self: s._handle_change(c), "value")
                        self.cells.append([cell_0, cell_1])
                    else:
                        self.cells[i][0].value = k
                        self.cells[i][1].value = v
                    i = i+1
                if self._table.rows < len(self.cells):
                    self.cells = self.cells[: self._table.rows - len(self.cells) or None]
                self._table.cells = tuple([i for i in self._table.cells if i.row_start < self._table.rows])
        return proposal['value']
    
    @validate('description')
    def _valid_description(self, proposal):
        self._label.value = proposal['value']
        return proposal['value']
a = DictSheet(description = "asd", value={'s':'s', "r":3})
    
              