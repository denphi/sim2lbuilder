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

The user-facing components of the Cyberinfrastructure (CI) ecosystem, science gateways and scientific workflow systems,
share a common need of interfacing with physical resources (storage systems and execution environments) to manage data and execute codes (applications).

However, there is no uniform, platform-independent way to describe either the resources or the applications. To address this, we propose uniform semantics for describing resources and applications that will be relevant to a diverse set of stakeholders.

The SGCI Resource Description Specification provides a standard way for institutions and service providers to describe storage and computing infrastructure broadly available to the research computing and science gateway community. SGCI Resource descriptions provide a foundation for interoperability across gateway components and other cyberinfrastructure software.

The current, initial version of the resource description language focuses on “traditional” HPC and high-throughput storage and computing resources

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