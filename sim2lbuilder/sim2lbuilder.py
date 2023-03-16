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
import re
import os
from IPython.display import display
from traitlets import Dict, validate, Unicode, List, Instance
from ipywidgets import VBox, HBox, Label, Output, FileUpload, HTML, Textarea, Layout
from IPython.display import FileLink
from PIL import Image
import io, json
import inspect

from nanohubuidl.material import MaterialBuilder
from nanohubuidl.material import MaterialContent
from nanohubuidl.plotly import PlotlyBuilder
from nanohubuidl.nanohub import Auth
from nanohubuidl.ipywidgets import buildWidget
from nanohubuidl.teleport import TeleportGlobals
from nanohubuidl.teleport import TeleportProject, TeleportElement, TeleportContent
from nanohubuidl.teleport import TeleportStatic, TeleportConditional

from .utils import buildParams, buildLayout
from .utils import deleteHistory, Settings
from .utils import loadDefaultSimulation

from .views import loadPlotly, loadMultiPlotly, loadSequencePlotly
from .views import loadTablePlotly, loadValuePlotly, loadHTML
from .views import squidDetail, refreshViews

from .components import Error, Loader
from .components import InputDict, InputList, InputNumber, InputInteger
from .components import InputChoice, InputText, InputBoolean, InputFile
from .components import AppBar, Results



class UIDLConstructor():
    
    STATE_LOADER_STATUS = "loader_status"
    STATE_LOADER_OPEN = "loader_open"
    STATE_ERROR_STATUS = "error_status"
    STATE_ERROR_OPEN = "error_open"
    
    def __init__(self, schema=None, **kwargs):
        self.schema = schema
        self.setup();
        self.theme = MaterialBuilder.DefaultTheme()
        self.appbar = AppBar(
            title=self.TOOLNAME
        )
        self.url = kwargs.get("url", "https://nanohub.org")
        self.drawer_width = kwargs.get("drawer_width", 250) 
        self.load_default = kwargs.get("load_default", False) 
        self.enable_compare = kwargs.get("enable_compare", True) 
        
        try :
            self.width = str(float(kwargs.get("width", "1024"))) + "px"
        except:
            self.width = str(kwargs.get("width", "1024px"))
        try :
            self.height = str(float(kwargs.get("height", "768"))) + "px"
        except:
            self.height = str(kwargs.get("height", "768px"))
        self.delay = kwargs.get("delay", 5000)

        self.globals = TeleportGlobals()
        loader = ".loader:empty {";
        loader +="position: absolute;";
        loader +="top: calc(50% - 4em);";
        loader +="left: calc(50% - 4em);";
        loader +="width: 6em;";
        loader +="height: 6em;";
        loader +="border: 1.1em solid #f1f1f1;";
        loader +="border-left: 1.1em solid #699FBB;";
        loader +="border-radius: 50%;";
        loader +="animation: load8 1.1s infinite linear;";
        loader +="}";
        self.globals.addAsset("loader", {"type": "style", "content": loader})
        animation ="@keyframes load8 {";
        animation +="0% {";
        animation +="transform: rotate(0deg);";
        animation +="}";
        animation +="100% {";
        animation +="transform: rotate(360deg);";
        animation +="}";
        animation +="}";
        self.globals.addAsset("animation", {"type": "style", "content": animation})
        
        self.components = {
            "InputDict" : InputDict(),
            "InputList" : InputList(),
            "InputNumber" : InputNumber(),
            "InputInteger" : InputInteger(),
            "InputChoice" : InputChoice(),
            "InputText" : InputText(),
            "InputBoolean" : InputBoolean(),
            "InputFile" : InputFile(),
        }
        
        self.views = {
            "loadPlotly" : {
                "state" : {'open_params':False,'open_details':False},
                "params" : ["dataset", "layout", "shapes"],
                "js":loadPlotly()
            },
            "loadMultiPlotly" : {
                "state" : {'open_params':False,'open_details':False},
                "params" : ["dataset", "layout", "shapes"],
                "js":loadMultiPlotly()
            },
            "loadSequencePlotly" : {
                "state" : {'open_params':False,'open_details':False},
                "params" : ["dataset", "layout", "normalize", "start_trace"],
                "js":loadSequencePlotly()
            },
            "loadTablePlotly" : {
                "state" : {'open_params':False,'open_details':False},
                "params" : ["dataset", "layout", "shapes"],
                "js":loadTablePlotly()
            },
            "loadValuePlotly" : {
                "state" : {'open_params':False,'open_details':False},
                "params" : ["dataset", "layout", "shapes"],
                "js":loadValuePlotly()
            },
            "loadHTML" : {
                "state" : {'open_params':False,'open_details':True},
                "params" : ["dataset"],
                "js":loadHTML()
            },
            "squidDetail" : {
                "state" : {},
                "params" : ["dataset"],
                "js":squidDetail(tn=self.TOOLNAME)
            }
        }
        
        self.SESSIONTOKEN = "SESSIONTOKEN"
        self.SESSIONID = "00000"
        try:
            if "SESSIONDIR" in os.environ:
                with open(os.environ["SESSIONDIR"]+"/resources") as file:
                    lines = [line.split(" ", 1) for line in file.readlines()]
                    properties = {line[0].strip(): line[1].strip() for line in lines if len(line)==2}
                    self.SESSIONTOKEN = properties["session_token"]
                    self.SESSIONID = properties["sessionid"]
        except:
            self.SESSIONTOKEN = "SESSIONTOKEN"
            self.SESSIONID = "00000"
        
    def setup(self):
        self.TOOLNAME = self.schema["name"]
        self.REVISION = self.schema["revision"]
        self.OUTFILE = re.sub(r'[^A-Z]', '', self.TOOLNAME.upper()) + ".HTML"
        self.params = buildParams(self.schema['inputs'])
        self.inputs_layout = buildLayout(self.schema['layout']['children']['inputs'])
        self.outputs = self.buildOutputs(self.schema['outputs'])

    def buildOutputs(self, schema):
        outputs = []
        for k,s in schema.items():
            out = {}
            out['id'] = k
            out['title'] = s.get("label",k)
            if s.get("type","None") == "output.Dict":                
                out['function'] = 'loadPlotly'
                out['dataset'] = {
                    k: {
                        'type': 'scatter',
                        'name' : k, 
                        'x': '$index$0',
                        'y': '$index$1',
                    }
                }
                out['layout'] = {'title': k}
                outputs.append(out) 
            elif s.get("type","None") in ["output.Array", "output.List"]:                
                out['function'] = 'loadPlotly'
                out['dataset'] = {
                    k: {                        
                        'type': 'scatter',
                        'name' : k, 
                        'y': '$value',
                    }
                }
                out['layout'] = {'title': k} 
                outputs.append(out) 
            elif s.get("type","None") in ["output.Tag","output.Choice"]:                
                out['function'] = 'loadTablePlotly'
                out['dataset'] = {
                    k: {
                        'header': {
                            'values': '$value',
                            'fill': {'color': 'gray'},
                        },
                        'cells':{
                            'values': '$value',
                        }                    
                    }
                }
                out['layout'] = {'title': k}
                outputs.append(out) 
            elif s.get("type","None") in ["output.Number","output.Boolean","output.Integer"]:                
                out['function'] = 'loadValuePlotly'
                out['dataset'] = {
                    k: {
                        'name' : k, 
                        'mode' : 'markers',
                        'y': '$' + str(k),
                        'type': 'scatter',
                        'marker' : {
                            'size' : 20,
                        },
                    }
                }
                out['layout'] = { 'title': k }
                outputs.append(out) 
            elif s.get("type",None) in ["output.Image"]:
                out['function'] = 'loadHTML'
                out['dataset'] = {
                    k: {
                        'type':'div', 
                        'style':'padding:10px', 
                        'children':[{
                            'type':'img',
                            'src':'$value',
                            'width':'100%'
                        }]
                    }
                }
                outputs.append(out) 
            elif s.get("type",None) in ["output.File"]:
                out['function'] = 'loadHTML'
                out['dataset'] = {
                    k: {
                        'type':'div', 
                        'style':'padding:10px', 
                        'children':[{
                            'type':'a',
                            'href':'$value',
                            'download' : k + ".dat",
                            'children':[{
                                'type':'div',
                                'textContent':k,
                                'style':'padding:10px;background-color:#AAA;color:#333;font-family:"Roboto","Helvetica","Arial", sans-serif;line-height: 1.5;'
                            }],
                            'style' : "text-decoration:none"
                        }]
                    }
                }
                outputs.append(out) 
            elif s.get("type",None) in ["output.Text"]:
                out['function'] = 'loadHTML'
                out['dataset'] = {
                    k: {
                        'type':'div', 
                        'style':'padding:10px', 
                        'children':[{
                            'type':'pre',
                            'textContent':'$value'
                        }]
                    }
                }
                outputs.append(out) 
            else:
                 warnings.warn( k + " is not supported by default")  
        return outputs
        
        
    def start(self):
        self.Project = TeleportProject(self.TOOLNAME + "-" + str(self.REVISION) )
        self.Project.root.node.content.style['width'] = str(self.width)
        self.Project.root.node.content.style['height'] = str(self.height)
        self.Project.root.node.content.style['border'] = "1px solid #DDD"
        self.Project.globals = self.globals
        self.Component = self.Project.root
        self.Component.addStateVariable("open_params", {"type":"boolean", "defaultValue": False})
        self.Component.addStateVariable("compare", {"type":"boolean", "defaultValue": False})
        self.Component.addStateVariable("auth", {"type":"boolean", "defaultValue": False})
        self.Component.addStateVariable("open_details", {"type":"boolean", "defaultValue": False})
        self.Component.addStateVariable("enable_history", {"type":"boolean", "defaultValue": False})
        self.Component.addStateVariable("src_detail", {"type":"object", "defaultValue": { '__html': '' }})        
        self.Component.addStateVariable("active_cache", {"type":"array", "defaultValue": []})
        self.Component.addStateVariable("lastCache", {"type":"string", "defaultValue": ""})
        for k,v in self.components.items():
            self.Project.components[k] = v
        
        self.ErrorMessage = Error( 
            self.Component, 
            error_status = UIDLConstructor.STATE_ERROR_STATUS,
            error_open = UIDLConstructor.STATE_ERROR_OPEN,
            is_open = False
        )
        self.Loader = Loader( 
            self.Component, 
            loader_status = UIDLConstructor.STATE_LOADER_STATUS,
            loader_open = UIDLConstructor.STATE_LOADER_OPEN,
            is_open = self.load_default==True
        )

        self.onRefreshViews = refreshViews(self.Project, 
                                           self.Component, 
                                           views=self.views,
                                           enable_compare=self.enable_compare)   
        self.onDeleteHistory = deleteHistory(self.Project, self.Component)
        
        for k,v in self.views.items():
            if "js" in v:
                self.Component.addPropVariable(k, {"type":"func", "defaultValue": v["js"]})    

        
        self.Login, CLogin = Auth.Session(
            self.Project,
            self.Component,
            sessiontoken = self.SESSIONTOKEN,
            sessionnum = self.SESSIONID,
            url = self.url + "/api/developer/oauth/token",   
        )
        self.Login.content.events["onAuth"] = [
            self.onRefreshViews[0],
            { "type": "stateChange", "modifies": "auth", "newState": True},
        ]

        self.Login.content.events["onError"]=[
            { "type": "stateChange", "modifies": "lastCache", "newState": ""},
            { "type": "stateChange", "modifies": UIDLConstructor.STATE_ERROR_OPEN, "newState": False},
            { "type": "stateChange", "modifies": UIDLConstructor.STATE_LOADER_OPEN, "newState": False},
        ]
        
        
        self.Frame = TeleportElement(TeleportContent(elementType="div"))
        self.Frame.content.style['position'] = "relative"
        self.Frame.content.style = {
            "position": "relative",
            "minHeight": "calc(" + str(self.height) + " - 130px)",
            "width": "100%",
            "flex" : "1",
            "overflow" : "auto"
        }

        self.Frame.content.attrs["dangerouslySetInnerHTML"] = {
            "type": "dynamic",
            "content": {
                "referenceType": "state",
                "id": "src_detail"
            }    
        }
        
        DetailsPanel2 = TeleportConditional(self.Frame)
        DetailsPanel2.reference = {"type": "static","content":'self.state.open_params'}
        DetailsPanel2.value = False
        DetailsPanel2.conditions =[{"operation" : "=="}]
        
        self.DetailsPanel = TeleportConditional(DetailsPanel2)
        self.DetailsPanel.reference = {"type": "static","content":'self.state.open_details'}
        self.DetailsPanel.value = True
        self.DetailsPanel.conditions =[{"operation" : "=="}]

        
        self.buildBasePlot();

        
    def buildBasePlot(self):
        BasePlot = PlotlyBuilder.BasePlot(self.Project, self.Component)
        BasePlot.content.style = {
            "position": "relative",
            "minHeight": "calc(" + str(self.height) + " - 130px)",
            "width": "100%",
        }
        
        self.CBasePlot = BasePlot
        elem = self.Project.components["BasePlotlyComponent"].node.content
        elem.attrs["config"] = {
          "type": "dynamic",
          "content": {
            "referenceType": "prop",
            "id": "config"
          }    
        }
        self.Project.components["BasePlotlyComponent"].propDefinitions["handlePurge"]["defaultValue"]="(e)=>{}"
    
    def getNeededOutputs(self):
        outputs = {}
        for output in self.outputs:
            if "dataset" in output:
                for k in output["dataset"].keys():
                    outputs[k] = k
            if "shapes" in output:
                for k in output["shapes"].keys():
                    outputs[k] = k
                    
        out = set()
        for k in list(outputs.keys()):
            for kk in k.split(","):
                out.add(kk)
        return list(out)
    
    def getType(self, v):   
        typev = v.get("type", "")
        if typev == "input.Integer":
            return "integer"
        elif typev == "input.Number":
            return "number"
        elif typev == "input.Boolean":
            return "boolean"
        elif typev == "input.Dict":
            return "dict"
        elif typev == "input.List" or v["type"] == "input.Array":
            return "array"
        return "string"

    def getValue(self, v):   
        typev = v.get("type", "")
        if typev == "input.Integer":
            return v.get("value", 0)
        elif typev == "input.Number":
            return v.get("value", 0.0)
        elif typev == "input.Boolean":
            return v.get("value", False)
        elif typev == "input.Dict":
            return v.get("value", {})
        elif typev == "input.List" or v["type"] == "input.Array":
            return v.get("value", [])
        return v.get("value", "")
    
    
    def buildParametersPanel(self):

        parameters = {}
        for k, v in self.schema['inputs'].items():
            if isinstance(k, str) == False or k.isnumeric():
                k = "_" + k
            parameters[k] = self.getValue(v)
        AppSettingsComponent = Settings(
            self.Project,
            self.Component,
            layout = self.inputs_layout,
            params = self.params,
            parameters = parameters,
            url=self.url + "/api/results/simtools",
            toolname=self.TOOLNAME,
            revision=self.REVISION,
            outputs=self.getNeededOutputs(),
            delay=self.delay
        )
        for k, v in self.schema['inputs'].items():
            if isinstance(k, str) == False or k.isnumeric():
                k = "_" + k
            AppSettingsComponent.addStateVariable(
                k, {"type": v, "defaultValue": self.getValue(v)}
            )
            if k in self.params.keys():
                self.params[k].content.events["change"] = [
                    {
                        "type": "propCall2",
                        "calls": "onChange",
                        "args": ["{'" + k + "':e}"],
                    },
                    {
                        "type": "stateChange",
                        "modifies": k,
                        "newState": "$e",
                    }
                ]
        
        AppSettingsComponent.addPropVariable(
            "parameters", {"type": "object", "defaultValue": {}}
        )

        
        if (self.load_default):
            self.loadDefaultSimulation = loadDefaultSimulation(self.Project, AppSettingsComponent);


        self.Project.components["AppSettingsComponent"] = AppSettingsComponent
        
        self.Component.addStateVariable(
            "parameters", {"type": "object", "defaultValue": parameters}
        )
        
        AppSettings = TeleportElement(
            TeleportContent(elementType="AppSettingsComponent")
        )
        AppSettings.content.attrs["parameters"] = {
            "type": "dynamic",
            "content": {"referenceType": "state", "id": "parameters"},
        }
        AppSettings.content.events["onChange"] = [
            {
                "type": "stateChange",
                "modifies": "parameters",
                "newState": "${...self.state.parameters, ...e}",
            }
        ]
        
        AppSettings.content.events["onError"] = [{
            "type": "stateChange",
            "modifies": "lastCache",
            "newState": ""
        }, {
            "type": "stateChange",
            "modifies": UIDLConstructor.STATE_LOADER_OPEN,
            "newState": False
        }, {
            "type": "stateChange",
            "modifies": UIDLConstructor.STATE_ERROR_OPEN,
            "newState": True
        }, {
            "type": "stateChange",
            "modifies": UIDLConstructor.STATE_ERROR_STATUS,
            "newState": '$e'
        }]
        AppSettings.content.events["click"] = [{
            "type": "stateChange",
            "modifies": UIDLConstructor.STATE_LOADER_OPEN,
            "newState": True
        }]

        AppSettings.content.events["onStatusChange"] = [{
            "type": "stateChange",
            "modifies": UIDLConstructor.STATE_LOADER_STATUS,
            "newState": "$e.target.value"
        }]

        AppSettings.content.events["onSuccess"] = [
            {
                "type": "stateChange",
                "modifies": "open_plot",
                "newState": '$self.state.visualization.id'
            },
            {
                "type": "stateChange",
                "modifies": UIDLConstructor.STATE_LOADER_OPEN,
                "newState": False
            },
            {
                "type": "stateChange",
                "modifies": "open_params",
                "newState": False
            },
            {
                "type": "stateChange",
                "modifies": "open_details",
                "newState": False
            },
            {
                "type": "stateChange",
                "modifies": "lastCache",
                "newState": "$arguments[1]",
                "callbacks": self.onRefreshViews
            }
        ]

        CAPPSettings = TeleportConditional(AppSettings)
        CAPPSettings.reference = {
            "type": "dynamic",
            "content": {
                "referenceType": "state",
                "id": "auth"
            }
        }
        CAPPSettings.value = True
        CAPPSettings.conditions =[{"operation" : "=="}]

        ParametersPanel = MaterialBuilder.ExpansionPanel(
            title="Parameters", 
            disabled=False, 
            expanded={
              "type": "dynamic",
              "content": {
                "referenceType": "state",
                "id": "open_params"
              }    
            }, 
            content=[CAPPSettings]
        )
        ParametersPanel.content.events['change'] = [
            { "type": "stateChange", "modifies": "open_params","newState": "$toggle"}
        ]
        ParametersPanel.content.style={"width":"100%"}
        return ParametersPanel
   
    def buildExpansionPanel(self):
        RESULTS = {}
        for output in self.outputs:
            if "visualization" not in self.Component.stateDefinitions:
                self.Component.addStateVariable("visualization", {
                    "type": "object",
                    "defaultValue": output
                })
            oid = output.get('id',None)
            RESULTS[oid] = {
                'title': output.get('title', oid),
                'action': {
                    "type": "stateChange",
                    "modifies": "visualization",
                    "newState": output,
                    "callbacks": self.onRefreshViews
                }
            }
        if "visualization" not in self.Component.stateDefinitions:
            self.Component.addStateVariable("visualization", {
                "type": "object",
                "defaultValue": {}
            })
            
        RESULTS["settings"] = {
            'title':'Settings',
            'action': [
                {
                    "type": "stateChange",
                    "modifies": "open_params",
                    "newState": True,
                },
                {
                    "type": "stateChange",
                    "modifies": "open_details",
                    "newState": False,
                },
            ]
        }
        
        self.Component.addStateVariable(
            "open_plot", {"type": "string", "defaultValue": list(RESULTS.keys())[0]}
        )
        APPResults = Results( 
            results = RESULTS,
            onClick = [{ "type": "stateChange", "modifies": UIDLConstructor.STATE_LOADER_OPEN,"newState": True }],
            onLoad = [
                { "type": "stateChange", "modifies": UIDLConstructor.STATE_LOADER_OPEN,"newState": False }
            ],
        )


        return APPResults

    
    def buildLowerBar(self):
        Text1 = TeleportStatic()
        Text1.content = "Compare"
        ToggleButton1 = TeleportElement(MaterialContent(elementType="ToggleButton"))
        ToggleButton1.content.attrs["value"] = "Compare"

        ToggleButton1.addContent(Text1)
        ToggleButton1.content.events['click'] = [
            { "type": "stateChange", "modifies": "compare" ,"newState": "$toggle", "callbacks" : self.onRefreshViews}
        ]
        ToggleButton1.content.attrs["selected"] = {
          "type": "dynamic",
          "content": {
            "referenceType": "state",
            "id": "compare"
          }    
        }

        Cond1 = TeleportConditional(ToggleButton1)
        Cond1.reference = {"type": "static","content":'self.state.enable_history'}
        Cond1.value = True
        Cond1.conditions =[{"operation" : "=="}]


        Text2 = TeleportStatic()
        Text2.content = "Clear history"
        ToggleButton2 = TeleportElement(MaterialContent(elementType="ToggleButton"))
        ToggleButton2.content.attrs["value"] = "Clear history"

        ToggleButton2.addContent(Text2)
        ToggleButton2.content.events['click'] = self.onDeleteHistory
        Cond2 = TeleportConditional(ToggleButton2)
        Cond2.reference = {"type": "static","content":'self.state.enable_history'}
        Cond2.value = True
        Cond2.conditions =[{"operation" : "=="}]

        ToggleButtonGroup = TeleportElement(MaterialContent(elementType="ToggleButtonGroup"))
        ToggleButtonGroup.addContent(Cond1)
        ToggleButtonGroup.addContent(Cond2)
        ToggleButtonGroup.content.style = { 
            'width' : '100%', 
            'flexDirection': 'column', 
            'display': 'inline-flex', 
            'backgroundColor' : '#CCC'
        }
        ToggleButtonGroup.content.attrs["orientation"] = "vertical"
        ToggleButtonGroup.content.attrs["exclusive"] = True

        LAppBar = TeleportElement(MaterialContent(elementType="Paper"))
        LAppBar.content.style = {'padding':'10px', 'backgroundColor' : '#DDD'}

        LAppBar.addContent(ToggleButtonGroup)
        return LAppBar
        
    def buildThemeProvider(self):
        Gridv2 = TeleportElement(MaterialContent(elementType="Grid"))
        Gridv2.content.attrs["container"] = True
        Gridv2.content.attrs["direction"] = "column"
        Gridv2.addContent(self.buildParametersPanel())
        Gridv2.addContent(self.DetailsPanel)
        Gridv2.addContent(self.CBasePlot)  
        #Gridv2.content.style['width'] = "calc(" + str(self.width) + " - " + str(self.drawer_width) + "px)"
        Gridv2.content.style['position'] = "relative"
        Gridv2.content.style['overflowX'] = "hidden"
        Gridv2.content.style['overflowY'] = "auto"
        Gridv2.content.style['flex'] = "1"
        Gridv2.content.style['height'] = "calc(-64px + " + str(self.height) + ")"

        Drawer = TeleportElement(MaterialContent(elementType="Paper"))
        Drawer.addContent(self.buildExpansionPanel())
        Drawer.addContent(self.buildLowerBar())

        Drawer.content.style['position'] = "relative"
        #Drawer.content.style['width'] = "" + str(self.drawer_width) + "px"
        Drawer.content.style['height'] = "calc(-64px + " + str(self.height) + ")"
        Drawer.content.style['backgroundColor'] = "#EEE"
        Drawer.content.style['overflow'] = "auto"
        Drawer.content.style['flex'] = "0 0 " + str(self.drawer_width) + "px"

        Gridh = TeleportElement(MaterialContent(elementType="Grid"))
        Gridh.content.attrs["container"] = True
        Gridh.content.attrs["direction"] = "row" 
        Gridh.addContent(Drawer)
        Gridh.addContent(Gridv2)  

        Gridv = TeleportElement(MaterialContent(elementType="Grid"))
        Gridv.content.attrs["container"] = True
        Gridv.content.attrs["direction"] = "column"
        Gridv.addContent(self.appbar)
        Gridv.addContent(Gridh)

        ThemeProvider = MaterialBuilder.ThemeProvider( self.Component, self.theme )
        ThemeProvider.addContent(self.Login)
        ThemeProvider.addContent(self.ErrorMessage)
        ThemeProvider.addContent(self.Loader)
        ThemeProvider.addContent(Gridv)
        return ThemeProvider
        
    def assemble(self, **kwargs):
        if kwargs.get("uidl_local",False):
            if kwargs.get("jupyter_notebook_url",None) is not None:
                bp = os.readlink('/proc/%s/cwd' % os.environ['JPY_PARENT_PID'])
                ap = os.path.abspath(".")
                if ap.startswith(bp):
                    link = "/".join(kwargs.get("jupyter_notebook_url",None).split("/", 8)[:7])
                    link += "/uidl/UIDL.HTML/local"
                    self.url = link
                else:
                    print(" Dont have access to the file")
        self.start();
        self.Component.addNode(self.buildThemeProvider())
        if (kwargs.get("widget",False)):
            ComponentWidget = buildWidget(
                self.Project, 
                jupyter_axios=kwargs.get("jupyter_axios",False),
                debugger=kwargs.get("debugger",False), 
                verbose=kwargs.get("verbose",False)
            );
            return ComponentWidget()
        else:
            if (kwargs.get("jupyter_notebook_url",None) is not None):
                self.Project.buildReact(
                    self.OUTFILE, 
                    copy_libraries=kwargs.get("copy_libraries",False), 
                    run_uidl="local", 
                    jupyter_notebook_url = kwargs.get("jupyter_notebook_url","")
                )
            else:
                self.Project.buildReact(
                    self.OUTFILE, 
                    copy_libraries=kwargs.get("copy_libraries",False)
                )
        
   
            
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
        import simtool
        stl = simtool.searchForSimTool(widget.toolname)
        inputs = simtool.getSimToolInputs(stl)
        for i,w in widget.inputs.items():
            inputs[i].value = w.value
        r = simtool.Run(stl, inputs)
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
    stl = simtool.searchForSimTool(tool)
    if (stl['notebookPath'] == None):
        raise Exception("Simtool is not valid")
    if (stl['published'] == False):
        warnings.warn("sim2l is not published")
        name = stl['notebookPath'].replace("/","+")
        
    inputs = simtool.getSimToolInputs(stl)
    outputs = simtool.getSimToolOutputs(stl)
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

