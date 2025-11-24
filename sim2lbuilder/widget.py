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

import simtool as st
import warnings
import importlib
import re
import os
from IPython.display import display
from traitlets import Dict, validate, Unicode, List, Instance
from ipywidgets import VBox, HBox, Label, Output, FileUpload, HTML, Textarea, Layout
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
        self.RunSimTool = WidgetConstructor.defaultRunSimTool
        if 'name' in layx:
            self.toolname = layx['name']
        else:
            self.toolname = ""
        self.name = kwargs.get("widget_name","MyWidget")

        for item, value in layx.items():
            if item == "inputs":
                self.buildParameters(value, self.inputs)  
            elif item == "outputs":
                self.buildParameters(value, self.outputs)  
            elif item == "layout":
                self._layout = self.buildLayout(value)  
            else:
                warnings.warn(item + " is ignored") 
        VBox.__init__(self, **kwargs);
        
    def defaultRunSimTool (widget, *kargs):
        import simtool as st
        stl = st.searchForSimTool(widget.toolname)
        inputs = st.getSimToolInputs(stl)
        for i,w in widget.inputs.items():
            inputs[i].value = w.value
        r = st.Run(stl, inputs)
        for outk, out in widget.outputs.items():
            with out:
                print(r.read(outk))
                
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
                        if value2.startswith("input."):
                            if value2 == "input.Integer":
                                type_ = "BoundedIntText"
                            elif value2 == "input.Number":
                                type_ = "BoundedFloatText"
                            elif value2 == "input.Boolean":
                                type_ = "ToggleButton"
                            elif value2 == "input.List":
                                type_ = "ListSheet"
                                module_ = "sim2lbuilder"
                            elif value2 == "input.Array":
                                type_ = "ListSheet"
                                module_ = "sim2lbuilder"
                            elif value2 == "input.Dict":
                                type_ = "DictSheet"
                                module_ = "sim2lbuilder"
                            elif value2 == "input.Choice":
                                type_ = "Dropdown"
                            elif value2 == "input.Image":
                                type_ = "ImageUpload"
                                module_ = "sim2lbuilder"
                            else:
                                type_ = "Text"
                        elif value2.startswith("output."):
                            type_ = "Output"
                        else:
                            type_ = value2
                    elif item2 == "click":
                        click_ = value2
                    elif item2 == "module":
                        module_ = value2
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
    """Lookup simtool's schema by its name.
    
        Args:
            simtool_name (str): SimTool name.

            **button_click (str) : name of the function callback in the schema (Default "RunSimTool").

            **button_description (str): name of describing callback in the schema (Default "Run SimTool")

            **outputs_layout (str): layout container (Default "Accordeon")

            **output (any): if passed the schema will only return this part of the schema, e.g 'inputs' (Default None)

        Returns:
            A simToolSchema dictionary containing.

                name - the name of the simtool notebook if exists.

                revision - the simtool revision (if installed or published).

                inputs - the simtool inputs .

                outputs - the simtool outputs .

                layout - suggested containers layout for inputs and outputs.
    """
    schema = simtool_constructor(None, type('Node', (object,), {"value" :simtool_name}))
    dict_schema =  {
        'name': schema['name'],
        'revision': schema['revision'],
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
    name = tool
    stl = st.searchForSimTool(tool)
    if (stl['notebookPath'] == None):
        raise Exception("Simtool is not valid")
    if (stl['published'] == False):
        warnings.warn("sim2l is not published")
        name = stl['notebookPath'].replace("/","+")
        
    inputs = st.getSimToolInputs(stl)
    outputs = st.getSimToolOutputs(stl)
    if stl['simToolRevision'] is not None:
        revision = stl['simToolRevision'].replace("r", "")
    else:
        revision = "0"

    res = {'inputs':{},'outputs':{}, 'revision':revision, 'name':name}
    for i in inputs:
        if inputs[i].type in [None]:
            pass;
        elif inputs[i].type == "Element":
            res['inputs'][i] = {}
            res['inputs'][i]["type"] = ".Text"
            res['inputs'][i]["value"] = inputs[i]._e.name
            res['inputs'][i]["description"] = inputs[i].description
        else:
            res['inputs'][i] = {}
            for j in inputs[i]:
                if inputs[i][j] is None:
                    pass;
                elif j == "type":
                    res['inputs'][i][j] = "input." + inputs[i][j]
                elif j == "desc":                 
                    res['inputs'][i]["description"] = inputs[i][j]
                elif j == "units":
                    try:
                        res['inputs'][i][j] = str(inputs[i][j])
                    except:
                        res['inputs'][i][j] = ""
                else :
                    res['inputs'][i][j] = inputs[i][j]
           
    for i in outputs:
        res['outputs'][i] = {}
        if outputs[i].type in [None]:
            pass;
        else:
            for j in outputs[i]:
                if j == "type":
                    res['outputs'][i][j] = "output." + outputs[i][j]
                elif j == "units":
                    try:
                        res['inputs'][i][j] = str(outputs[i][j])
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
        self._table = Textarea(
            value=json.dumps(kwargs.get("value", [])),
            placeholder='AddList',
            disabled=False,
            layout=Layout(width="100%")
        )
        self._table.observe(lambda c, s=self: s._handle_change(c), "value")
        self._label = HTML(value=kwargs.get("description", "")) ##Label
        self.value = kwargs.get("value", [])
        kwargs["children"] = [self._label, self._table]
        HBox.__init__(self, **kwargs);

    def _handle_change(self, change):
        try:
            table = json.loads(self._table.value)
            self.value = table
            self._table.layout.border="1px solid #000"
        except:
            self._table.layout.border="3px solid #F00"

        
    @validate('value')
    def _valid_value(self, proposal):
        if isinstance(proposal['value'], dict):
            try:
                self._table.value = json.dumps(proposal['value'])
                self._table.layout.border="1px solid #000"
            except:
                self._table.layout.border="3px solid #F00"
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
        self._table = Textarea(
            value=json.dumps(kwargs.get("value", [])),
            placeholder='AddList',
            disabled=False,
            layout=Layout(width="100%")
        )
        self._table.observe(lambda c, s=self: s._handle_change(c), "value")
        self._label = HTML(value=kwargs.get("description", "")) ##Label
        self.value = kwargs.get("value", [])
        kwargs["children"] = [self._label, self._table]
        HBox.__init__(self, **kwargs);

    def _handle_change(self, change):
        try:
            table = json.loads(self._table.value)
            self.value = table
            self._table.layout.border="1px solid #000"
        except:
            self._table.layout.border="3px solid #F00"

        
    @validate('value')
    def _valid_value(self, proposal):
        if isinstance(proposal['value'], list):
            try:
                self._table.value = json.dumps(proposal['value'])
                self._table.layout.border="1px solid #000"
            except:
                self._table.layout.border="3px solid #F00"
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
