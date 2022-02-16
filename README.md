# Sim2lBuilder Stats

<table>
    <tr>
        <td>Latest Release</td>
        <td>
            <a href="https://pypi.org/project/sim2lbuilder/"/>
            <img src="https://badge.fury.io/py/sim2lbuilder.svg"/>
        </td>
    </tr>
    <tr>
        <td>PyPI Downloads</td>
        <td>
            <a href="https://pepy.tech/project/sim2lbuilder"/>
            <img src="https://pepy.tech/badge/sim2lbuilder/month"/>
        </td>
    </tr>
</table>

#Simtool Builder


## Introduction

sim2lbuilder is an utility library to create Graphical User interfaces on Jupyter notebooks.
sim2lbuilder is based on ipywidgets, and allow users to describe Apps based on their inputs, outputs and layout. Callback functions can also be referenced to be triggered by events on the widgets
sim2lbuilder can display described tools as widgets, or generate python code to be modified.

## Installation


```bash
pip install sim2lbuilder
```


## Usage


```python
schema = {
  'inputs': { 
    'n1': { 'type': 'IntText', 'value': 1}, 
    'n2': { 'type': 'IntText', 'value': 3}
  },
  'outputs': { 
    'sol': { 'type': 'IntText'}, 
  },
  'layout': { 
    'type': 'HBox',
    'children' : {
      'n1': None,
      'n2': None,
      'button' : {
        'type': 'Button',
        'click': 'SUM',
        'description': '=',
      },
      'sol': None
    }
  }
}
from sim2lbuilder import WidgetConstructor
s = WidgetConstructor(schema)
def SUM (w):
    w.outputs["sol"].value = w.inputs["n1"].value + w.inputs["n2"].value
s.SUM = SUM
s.assemble()
SUM(s)
display(s)

```

## Create a Sim2l GUI (Widget) 


```python
from sim2lbuilder import WidgetConstructor, GetSimtoolDefaultSchema
from simtool import searchForSimTool, getSimToolInputs, Run
schema = GetSimtoolDefaultSchema("meltingkim")
def RunSimTool(widget, *kargs):
    stl = searchForSimTool("meltingkim")
    inputs =getSimToolInputs(stl)
    for i,w in widget.inputs.items():
        inputs[i].value = w.value
    r =Run(stl, inputs)
    for outk, out in widget.outputs.items():
        with out:
            print(r.read(outk))
s = WidgetConstructor(schema)
s.RunSimTool = RunSimTool
s.assemble()
s

```

## Create a Sim2l GUI (Generate Code) 


```python
from sim2lbuilder import WidgetConstructor, GetSimtoolDefaultSchema
from simtool import searchForSimTool, getSimToolInputs, Run
schema = GetSimtoolDefaultSchema("meltingkim")
def RunSimTool(widget, *kargs):
    stl = searchForSimTool("meltingkim")
    inputs =getSimToolInputs(stl)
    for i,w in widget.inputs.items():
        inputs[i].value = w.value
    r =Run(stl, inputs)
    for outk, out in widget.outputs.items():
        with out:
            print(r.read(outk))
s = WidgetConstructor(schema, format="file")
s.RunSimTool = RunSimTool
s.assemble()
s

```

## Create a Sim2l GUI (Print Code) 


```python
from sim2lbuilder import WidgetConstructor, GetSimtoolDefaultSchema
from simtool import searchForSimTool, getSimToolInputs, Run
schema = GetSimtoolDefaultSchema("meltingkim")
def RunSimTool(widget, *kargs):
    stl = searchForSimTool("meltingkim")
    inputs =getSimToolInputs(stl)
    for i,w in widget.inputs.items():
        inputs[i].value = w.value
    r =Run(stl, inputs)
    for outk, out in widget.outputs.items():
        with out:
            print(r.read(outk))
s = WidgetConstructor(schema, format="text")
s.RunSimTool = RunSimTool
s.assemble()
s

```