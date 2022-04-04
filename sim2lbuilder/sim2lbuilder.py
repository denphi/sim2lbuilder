#  Copyright 2021 nanoHUB

#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

#  Authors:
#  Daniel Mejia (denphi), Purdue University (denphi@denphi.com)

import warnings
import importlib
import simtool
from IPython.display import display
from traitlets import Dict, validate, Unicode, List, Instance
from ipywidgets import VBox, HBox, Label, Output, FileUpload, HTML
import ipysheet
from IPython.display import FileLink
from PIL import Image
import io, json
import inspect


class WidgetConstructor(VBox):
    def __init__(self, layx=None, **kwargs):
        self.inputs = {}
        self.outputs = {}
        self.libraries = {"ipywidgets":[]}
        self.containers = {}
        self.clicks = []
        self.methods = []
        self.format = kwargs.get("format","object")
        self.widget_name = kwargs.get("widget_name","MyWidget")
        for item, value in layx.items():
            if item == "inputs":
                self.buildParameters(value, self.inputs)  
            elif item == "outputs":
                self.buildParameters(value, self.outputs)  
            elif item == "layout":
                self._layout = self.buildLayout(value)  
            else:
               pass;#warnings.warn(item + " is ignored") 
        VBox.__init__(self, **kwargs);
            
    def assemble(self):
        if self.format=="object":
            self.children = [self._layout]
            
        elif self.format=="text" or self.format=="file":
            textobject = ""
            for v in self.libraries.keys():
                textobject += "import " + str(v) + "\n"
            textobject += "class " + self.widget_name + "(ipywidgets.VBox):\n"
            textobject += "  def __init__(self, **kwargs):\n"
            textobject += "    self.inputs = {};\n"
            textobject += "    self.outputs = {};\n"
            textobject += "    self.containers = {};\n"
            for k,v in self.containers.items():
                textobject += "    self.containers['"+k+"'] = "+v+";\n"
            for k,v in self.inputs.items():
                textobject += "    self.inputs['"+k+"'] = "+v+";\n"
            for k,v in self.outputs.items():
                textobject += "    self.outputs['"+k+"'] = "+v+";\n"
            for v in self.clicks:
                textobject += "    "+v+";\n"
            textobject += "    ipywidgets.VBox.__init__(self, **kwargs);\n"
            textobject += "    self.children = [" + self._layout+"];\n"
            for m in self.methods:
                try:
                    lines = inspect.getsource(getattr(self, m))
                    for l in lines.split('\n'):
                        textobject += "  " + l + "\n"
                except:
                    pass;
            if self.format=="text":
                self.children = [HTML(value="<pre>" + textobject+"</pre>")]
            else:
                f = open(self.widget_name + ".py", "w")
                f.write(textobject)
                f.close()
                self.children = [HTML(value="<a href='"+ self.widget_name + ".py"+"' target='blank'>Download File</a>")]
        else:
            raise Except("Format not valid")
            
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
                        try:
                            value2j = json.dumps(value2)
                            if value2j != "null":
                                params_[item2] = value2
                        except:
                            pass;
                uuid = "cont" + str(len(self.containers.keys()))        
                if self.format=="object":
                    module = importlib.import_module(module_)
                    class_ = getattr(module, type_)
                    self.containers[uuid] = class_(**params_) 
                    storage[item] = self.containers[uuid]
                    self.setClick(storage[item], click_)                
                
                elif self.format=="text" or self.format=="file":
                    if module_ not in self.libraries:
                        self.libraries[module_] = {}
                    for k,v in params_.items():
                        if (v is True):
                           params_[k] = "True"
                        elif (v is False):
                           params_[k] = "False" 
                        else:
                           params_[k] = json.dumps(v) 
                    self.containers[uuid] = module_+"."+type_+"(" + ",".join([str(k)+"="+v for k,v in params_.items()])+ ")"
                    storage[item] = "self.containers['" + uuid+ "']"

                    if click_ is not None:
                        self.methods.append(click_) 
                        self.clicks.append("self.containers['" + uuid+ "'].on_click(lambda a, b=self, c='" + click_ + "' : getattr(b, c)(b))")                

                else:
                    raise Except("Format not valid")
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
                            if (item2.replace("input.","") in self.inputs):
                                child_ = self.inputs[item2.replace("input.","")]
                            elif (item2.replace("output.","") in self.outputs):
                                child_ = self.outputs[item2.replace("output.","")]
                            elif (item2 in self.inputs):
                                child_ = self.inputs[item2]
                            elif (item2 in self.outputs):
                                child_ = self.outputs[item2]
                            else :
                               warnings.warn(item2 + " is not a valid element")
                        else:
                            child_ = self.buildLayout(value2)
                        if child_ is not None:
                            children_.append(child_)
                elif type(value) == list:
                    for item2 in value:
                        child_ = None
                        if (item2.replace("input.","") in self.inputs):
                            child_ = self.inputs[item2.replace("input.","")]
                        elif (item2.replace("output.","") in self.outputs):
                            child_ = self.outputs[item2.replace("output.","")]
                        elif (item2 in self.inputs):
                            child_ = self.inputs[item2]
                        elif (item2 in self.outputs):
                            child_ = self.outputs[item2]
                        else :
                           warnings.warn(item2 + " is not a valid element")
                        if child_ is not None:
                            children_.append(child_)
                else:
                   warnings.warn(item + " is not a valid description")
            else:
                if self.format=="text" or self.format=="file":
                    params_[item] = json.dumps(value)
                else:
                    params_[item] = value
            
        uuid = "cont" + str(len(self.containers.keys()))
        if self.format=="object":        
            if (len(titles_) > 0 ):
                params_["titles"] = titles_
            if (len(children_) > 0 ):
                params_["children"] = children_
            module = importlib.import_module(module_)
            class_ = getattr(module, type_)
            self.containers[uuid] = class_(**params_) 
            instance_ = self.containers[uuid]
            self.setClick(instance_, click_)
            for i, title in enumerate(titles_):
                try:
                    instance_.set_title(i, title)
                except:
                   warnings.warn(title + " can not be assigned")
                
        elif self.format=="text" or self.format=="file":
            if (len(titles_) > 0 ):
                params_["titles"] =  "['" + "','".join(titles_) + "']"
            if (len(children_) > 0 ):
                params_["children"] = "[" + ",".join(children_) + "]"
            if module_ not in self.libraries:
                self.libraries[module_] = {}
            self.containers[uuid] = module_+"."+type_+"(" + ",".join([str(k)+"="+str(v) for k,v in params_.items()])+ ")"
            if click_ is not None:
                self.methods.append(click_) 
                self.clicks.append("self.containers['" + uuid+ "'].on_click(lambda a, b=self, c='" + click_ + "' : getattr(b, c)(b))")                
            instance_ = "self.containers['" + uuid+ "']"
        else:
            raise Except("Format not valid")
        return instance_
         
    def setClick(self, instance, function_name):
        if function_name is not None:
            instance.on_click(None, remove=True)
            instance.on_click(lambda a, b=self, c=function_name: getattr(b, c)(b))   
        
        
def GetSimtoolDefaultSchema( simtool_name, **kwargs ):
    schema = simtool_constructor(None, type('Node', (object,), {"value" :simtool_name}))
    dict_schema =  {
        'inputs': schema['inputs'],
        'outputs': schema['outputs'],
        'layout':{
            'type': 'HBox',
            'children' : { 
                'inputs' : {
                    'layout':{
                        'width' : 'auto'
                    },
                    'type': 'VBox',
                    'children' : ["input."+str(c) for c in schema['inputs'].keys()]
                },
                'outputs' : {
                    'type': 'VBox',
                    'children':{ 
                        'button':{
                            'type' : 'Button',
                            'click' : kwargs.get('button_click','RunSimTool'),
                            'description' : kwargs.get('button_description','Run SimTool')
                        }, 'container' : {
                            'type': kwargs.get('outputs_layout','Accordion'),
                            'children' : ["output."+str(c) for c in schema['outputs'].keys()],
                            'titles': [c for c in schema['outputs'].keys()]
                        }
                    },
                    'layout':{
                        'flex':'1'
                    }
                }
            }
        }
    }
    output = kwargs.get('output',None)
    if output in dict_schema.keys():
        dict_schema = dict_schema[output]
        
    return dict_schema
        

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
        raise Except("Simtool is not valid")
    inputs = simtool.getSimToolInputs(stl)
    outputs = simtool.getSimToolOutputs(stl)
    res = {'inputs':{},'outputs':{}}
    for i in inputs:
        if inputs[i].type in [None]:
            pass;
        elif inputs[i].type == "Element":
            res['inputs'][i] = {}
            res['inputs'][i]["type"] = "Text"
            res['inputs'][i]["value"] = inputs[i]._e.name
            res['inputs'][i]["description"] = inputs[i].description
        else:
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
                    elif inputs[i][j] == "List" or inputs[i][j] == "Array":
                        res['inputs'][i][j] = "ListSheet"
                        res['inputs'][i]["module"] = "sim2lbuilder"
                    elif inputs[i][j] == "Dict":
                        res['inputs'][i][j] = "DictSheet"
                        res['inputs'][i]["module"] = "sim2lbuilder"
                    elif inputs[i][j] == "Choice":
                        res['inputs'][i][j] = "Dropdown"
                    elif inputs[i][j] == "Image":
                        res['inputs'][i][j] = "ImageUpload"
                        res['inputs'][i]["module"] = "sim2lbuilder"

                    else:
                        res['inputs'][i][j] = "Text"
                elif j == "desc":                 
                    res['inputs'][i]["description"] = inputs[i][j]
                elif j == "units":
                    try:
                        res['inputs'][i][j] = inputs[i][j].__str__()
                    except:
                        res['inputs'][i][j] = ""
                else :
                    res['inputs'][i][j] = inputs[i][j]
           
    for i in outputs:
        res['outputs'][i] = {}
        for j in outputs[i]:
            if j == "type":
                res['outputs'][i][j] = "Output"
            elif j == "units":
                try:
                    res['outputs'][i][j] = inputs[i][j].__str__()
                except:
                    res['outputs'][i][j] = ""
            else:
                res['outputs'][i][j] = outputs[i][j]
    if path != "":
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
        self.debug = Output()
        self._table = ipysheet.Sheet(columns = 2, row_headers = False, column_headers = ["key", "value"])
        self._label = HTML(value=kwargs.get("description", "")) ##Label
        self.updating = False
        self.value = kwargs.get("value", {})
        kwargs["children"] = [self._label, self._table]
        HBox.__init__(self, **kwargs);
   
    def _handle_change(self, change):
        if self.updating is False:
            table = [[0,0] for i in range(self._table.rows)]
            for cell in self._table.cells:
                if cell.value == None:
                    table[cell.row_start][cell.column_start] = ""
                else :
                    table[cell.row_start][cell.column_start] = cell.value
            new_dict = {i[0]:i[1] for i in table if i[0] != ""}
            self.value = new_dict
        
    @validate('value')
    def _valid_value(self, proposal):
        if isinstance(proposal['value'], dict):
            self._table.rows = len(proposal['value'].keys()) + 1
            for i in range(self._table.rows):
                if i >= len(self._table.cells)/2:
                    cell_0 = ipysheet.Cell(row_start=i,row_end=i, column_start=0, column_end=0, value="", type="text", choice=None)
                    cell_0.observe(lambda c, s=self: s._handle_change(c), "value")
                    self._table.cells = self._table.cells+(cell_0,)
                    cell_1 = ipysheet.Cell(row_start=i,row_end=i, column_start=1, column_end=1, value="", type="text", choice=None)
                    cell_1.observe(lambda c, s=self: s._handle_change(c), "value")
                    self._table.cells = self._table.cells+(cell_1,)
            self._table.cells = tuple([i for i in self._table.cells if i.row_start < self._table.rows])

            if self.updating is False:
                self.updating = True
                i=0
                for k,v in proposal['value'].items():
                    if (self._table.cells[i*2+1].value != v):
                        self._table.cells[i*2+1].value = v
                    if (self._table.cells[i*2].value != k):
                        self._table.cells[i*2].value = k
                    i = i + 1
                self._table.cells[i*2].value = ""
                self._table.cells[i*2+1].value = ""
            self.updating = False
        return proposal['value']
    
    @validate('description')
    def _valid_description(self, proposal):
        self._label.value = proposal['value']
        return proposal['value']
    
class ListSheet(HBox):
    value = List([]).tag(sync=True)
    description = Unicode("").tag(sync=True)
    def __init__(self, **kwargs):
        self.debug = Output()
        self._table = ipysheet.Sheet(columns = 1, row_headers = False, column_headers = ["value"])
        self._label = HTML(value=kwargs.get("description", "")) ##Label
        self.updating = False
        self.value = kwargs.get("value", [])
        kwargs["children"] = [self._label, self._table]
        HBox.__init__(self, **kwargs);
   
    def _handle_change(self, change):
        if self.updating is False:
            table = []
            for i, cell in enumerate(self._table.cells):
                if (cell.value == None or cell.value == ""):
                    pass;
                else :
                    table.append(cell.value)
            self.value = table
        
    @validate('value')
    def _valid_value(self, proposal):
        if isinstance(proposal['value'], list):
            self._table.rows = len(proposal['value']) + 1
            for i in range(self._table.rows):
                if i >= len(self._table.cells):
                    cell_0 = ipysheet.Cell(row_start=i,row_end=i, column_start=0, column_end=0, value="", type="text", choice=None)
                    cell_0.observe(lambda c, s=self: s._handle_change(c), "value")
                    self._table.cells = self._table.cells+(cell_0,)
            self._table.cells = tuple([i for i in self._table.cells if i.row_start < self._table.rows])

            if self.updating is False:
                self.updating = True
                i=0
                for k in proposal['value']:
                    if (self._table.cells[i].value != k):
                        self._table.cells[i].value = k
                    i = i + 1
                self._table.cells[i].value = ""
            self.updating = False
        return proposal['value']
    
    @validate('description')
    def _valid_description(self, proposal):
        self._label.value = proposal['value']
        return proposal['value']


class ImageUpload(HBox):
    value = Instance(Image.Image).tag(sync=False)
    description = Unicode("").tag(sync=True)
    def __init__(self, **kwargs):
        self.debug = Output()
        self._upload = FileUpload(accept='image/*',multiple=False)
        self._upload.observe(lambda c, s=self: ImageUpload._handle_change(s, c), names='_counter')
        self._label = HTML(value=kwargs.get("description", "")) ##Label
        self.updating = False
        self.value = kwargs.get("value", Image.open("nanohub.png"))
        kwargs["children"] = [self._label, self._upload]
        HBox.__init__(self, **kwargs);
   
    def _handle_change(self, change):
        if self._upload._counter > 0 :
            content = list(self._upload.value.values())[0]['content']
            name = list(self._upload.value.values())[0]['metadata']['name']
            self.value = Image.open(io.BytesIO(content))
            self._upload._counter = 0
        
    
    @validate('description')
    def _valid_description(self, proposal):
        self._label.value = proposal['value']
        return proposal['value']

