from nanohubuidl.teleport import TeleportComponent, TeleportElement, TeleportContent
from nanohubuidl.teleport import TeleportStatic, TeleportRepeat, TeleportDynamic
from nanohubuidl.material import MaterialContent

def InputDict():
    name = "InputDict"
    string = TeleportElement(MaterialContent(elementType="TextField"))
    string.content.attrs["variant"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "variant"},
    }
    string.content.attrs["label"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "label"},
    }
    string.content.attrs["fullWidth"] = True
    string.content.attrs["helperText"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "description"},
    }
    string.content.style = {"margin": "10px 0px 10px 0px"}
    string.content.attrs[
        "dummy"
    ] = "$self.props.onDefault(self, self.props.value)"
    string.content.attrs["value"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "value"},
    }
    string.content.attrs["disabled"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "disabled"},
    }
    string.content.events["change"] = []
    string.content.events["change"].append(
        {"type": "propCall2", "calls": "onValidate", "args": ["self", "e.target.value"]}
    )
    string.content.events["blur"] = []
    string.content.events["blur"].append(
        {"type": "propCall2", "calls": "onBlur", "args": ["self", "e.target.value"]}
    )
    string.content.attrs["error"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "error"},
    }

    Component = TeleportComponent(name, string)

    Component.addStateVariable("error", {"type": "boolean", "defaultValue": False})
    Component.addStateVariable(
        "value", {"type": "string", "defaultValue": "$JSON.stringify(self.props.value)"}
    )
    Component.addStateVariable(
        "lastDefault",
        {"type": "string", "defaultValue": "$JSON.stringify(self.props.value)"},
    )

    Component.addPropVariable("variant", {"type": "string", "defaultValue": "outlined"})
    Component.addPropVariable("label", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("description", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("disabled", {"type": "boolean", "defaultValue": False})
    Component.addPropVariable("value", {"type": "object", "defaultValue": {}})
    Component.addPropVariable("onChange", {"type": "func", "defaultValue": "(e)=>{}"})
    Component.addPropVariable(
        "onDefault",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            let a = JSON.stringify(e); 
            if (s.state && a!=s.state.lastDefault)
                s.setState({'lastDefault':a, 'value':a});
            return a;
        }""",
        },
    )

    Component.addPropVariable(
        "onValidate",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            try {
                let v=JSON.parse(e); 
                if (typeof v !== 'object') { 
                    throw 'Not Object';
                } 
                s.setState({'error':false,'value':e});
            }catch(ee){
                s.setState({'error':true,'value':e})
            }
        }""",
        },
    )

    Component.addPropVariable(
        "onBlur",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            try {
                let v=JSON.parse(e); 
                if (typeof v !== 'object') { 
                    throw 'Not Object';
                } 
                s.setState({'error':false,'value':e});
                s.props.onChange(v)
            }catch(ee){
                s.setState({'error':false,'value':s.state.lastDefault});
            }
        }""",
        },
    )
    return Component


def InputList():
    name = "InputList"
    string = TeleportElement(MaterialContent(elementType="TextField"))
    string.content.attrs["variant"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "variant"},
    }
    string.content.attrs["label"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "label"},
    }
    string.content.attrs["fullWidth"] = True
    string.content.attrs["helperText"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "description"},
    }
    string.content.style = {"margin": "10px 0px 10px 0px"}
    string.content.attrs[
        "dummy"
    ] = "$self.props.onDefault(self, self.props.value)"
    string.content.attrs["value"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "value"},
    }
    string.content.events["change"] = []
    string.content.events["change"].append(
        {"type": "propCall2", "calls": "onValidate", "args": ["self", "e.target.value"]}
    )
    string.content.attrs["disabled"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "disabled"},
    }
    string.content.events["blur"] = []
    string.content.events["blur"].append(
        {"type": "propCall2", "calls": "onBlur", "args": ["self", "e.target.value"]}
    )
    string.content.attrs["error"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "error"},
    }

    Component = TeleportComponent(name, string)

    Component.addStateVariable("error", {"type": "boolean", "defaultValue": False})
    Component.addStateVariable(
        "value", {"type": "string", "defaultValue": "$JSON.stringify(self.props.value)"}
    )
    Component.addStateVariable(
        "lastDefault",
        {"type": "string", "defaultValue": "$JSON.stringify(self.props.value)"},
    )

    Component.addPropVariable("variant", {"type": "string", "defaultValue": "outlined"})
    Component.addPropVariable("label", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("description", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("disabled", {"type": "boolean", "defaultValue": False})
    Component.addPropVariable("value", {"type": "array", "defaultValue": []})
    Component.addPropVariable("onChange", {"type": "func", "defaultValue": "(e)=>{}"})
    Component.addPropVariable(
        "onDefault",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            let a = JSON.stringify(e); 
            if (s.state && a!=s.state.lastDefault)
                s.setState({'lastDefault':a, 'value':a});
            return a;
        }""",
        },
    )
    Component.addPropVariable(
        "onValidate",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            try {
                let v=JSON.parse(e); 
                if (!Array.isArray(v)) { 
                    throw 'Not Array';
                } 
                s.setState({'error':false,'value':e});
            }catch(ee){
                s.setState({'error':true,'value':e})
            }
        }""",
        },
    )

    Component.addPropVariable(
        "onBlur",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            try {
                let v=JSON.parse(e); 
                if (!Array.isArray(v)) { 
                    throw 'Not Array';
                } 
                s.setState({'error':false,'value':e});
                s.props.onChange(v)
            }catch(ee){
                s.setState({'error':false,'value':s.state.lastDefault});
            }
        }""",
        },
    )
    return Component


def InputNumber():
    name = "InputNumber"
    string = TeleportElement(MaterialContent(elementType="TextField"))
    string.content.attrs["variant"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "variant"},
    }
    string.content.attrs["label"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "label"},
    }
    string.content.attrs["fullWidth"] = True
    string.content.attrs["helperText"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "description"},
    }
    string.content.style = {"margin": "10px 0px 10px 0px"}
    string.content.attrs[
        "dummy"
    ] = "$self.props.onDefault(self, self.props.value)"
    string.content.attrs["value"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "value"},
    }
    string.content.attrs["suffix"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "suffix"},
    }
    string.content.events["change"] = []
    string.content.events["change"].append(
        {"type": "propCall2", "calls": "onValidate", "args": ["self", "e.target.value"]}
    )
    string.content.events["blur"] = []
    string.content.events["blur"].append(
        {"type": "propCall2", "calls": "onBlur", "args": ["self", "e.target.value"]}
    )
    string.content.attrs["disabled"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "disabled"},
    }
    string.content.attrs["error"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "error"},
    }

    Component = TeleportComponent(name, string)

    Component.addStateVariable("error", {"type": "boolean", "defaultValue": False})
    Component.addStateVariable(
        "value", {"type": "string", "defaultValue": "$String(self.props.value)"}
    )
    Component.addStateVariable(
        "lastDefault", {"type": "string", "defaultValue": "$String(self.props.value)"}
    )

    Component.addPropVariable("variant", {"type": "string", "defaultValue": "outlined"})
    Component.addPropVariable("suffix", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("label", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("disabled", {"type": "boolean", "defaultValue": False})
    Component.addPropVariable("description", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("value", {"type": "number", "defaultValue": 0.0})
    Component.addPropVariable("min", {"type": "number", "defaultValue": None})
    Component.addPropVariable("max", {"type": "number", "defaultValue": None})
    Component.addPropVariable("onChange", {"type": "func", "defaultValue": "(e)=>{}"})
    Component.addPropVariable(
        "onDefault",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            let a = String(e); 
            if (s.state && a!=s.state.lastDefault)
                s.setState({'error':false,'lastDefault':a, 'value':a});
            return a;
        }""",
        },
    )

    Component.addPropVariable(
        "onValidate",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            try {
                let v = Number(e); 
                if (isNaN(v)) { 
                    throw 'Not Number';
                } 
                s.setState({'error':false,'value':e});
            }catch(ee){
                s.setState({'error':true,'value':e})
            }
        }""",
        },
    )

    Component.addPropVariable(
        "onBlur",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            try {
                let v = Number(e); 
                if (isNaN(v)) { 
                    throw 'Not Number';
                } 
                if (s.props.min && v < s.props.min) { 
                    v = s.props.min;
                    e = String(v);
                } 
                if (s.props.max && v > s.props.max) { 
                    v = s.props.max;
                    e = String(v);
                } 
                s.setState({'error':false,'value':e});
                s.props.onChange(v)
            }catch(ee){
                s.setState({'error':false,'value':s.state.lastDefault});
            }
        }""",
        },
    )
    return Component


def InputInteger():
    name = "InputInteger"
    string = TeleportElement(MaterialContent(elementType="TextField"))
    string.content.attrs["variant"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "variant"},
    }
    string.content.attrs["label"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "label"},
    }
    string.content.attrs["fullWidth"] = True
    string.content.attrs["decimalscale"] = 0
    string.content.attrs["helperText"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "description"},
    }
    string.content.style = {"margin": "10px 0px 10px 0px"}
    string.content.attrs[
        "dummy"
    ] = "$self.props.onDefault(self, self.props.value)"
    string.content.attrs["value"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "value"},
    }
    string.content.attrs["suffix"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "suffix"},
    }
    string.content.events["change"] = []
    string.content.events["change"].append(
        {"type": "propCall2", "calls": "onValidate", "args": ["self", "e.target.value"]}
    )
    string.content.events["blur"] = []
    string.content.events["blur"].append(
        {"type": "propCall2", "calls": "onBlur", "args": ["self", "e.target.value"]}
    )
    string.content.attrs["disabled"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "disabled"},
    }
    string.content.attrs["error"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "error"},
    }

    Component = TeleportComponent(name, string)

    Component.addStateVariable("error", {"type": "boolean", "defaultValue": False})
    Component.addStateVariable(
        "value", {"type": "string", "defaultValue": "$String(self.props.value)"}
    )
    Component.addStateVariable(
        "lastDefault", {"type": "string", "defaultValue": "$String(self.props.value)"}
    )

    Component.addPropVariable("variant", {"type": "string", "defaultValue": "outlined"})
    Component.addPropVariable("suffix", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("disabled", {"type": "boolean", "defaultValue": False})
    Component.addPropVariable("label", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("description", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("value", {"type": "integer", "defaultValue": 0})
    Component.addPropVariable("min", {"type": "integer", "defaultValue": None})
    Component.addPropVariable("max", {"type": "integer", "defaultValue": None})
    Component.addPropVariable("onChange", {"type": "func", "defaultValue": "(e)=>{}"})
    Component.addPropVariable(
        "onDefault",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            let a = String(e); 
            if (s.state && a!=s.state.lastDefault)
                s.setState({'error':false,'lastDefault':a, 'value':a});
            return a;
        }""",
        },
    )

    Component.addPropVariable(
        "onValidate",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            try {
                let v = Number(e); 
                if (isNaN(v) || !Number.isInteger(v)) { 
                    throw 'Not Integer';
                } 
                s.setState({'error':false,'value':e});
            }catch(ee){
                s.setState({'error':true,'value':e})
            }
        }""",
        },
    )

    Component.addPropVariable(
        "onBlur",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            try {
                let v = Number(e); 
                if (isNaN(v)) { 
                    throw 'Not Integer';
                } 
                if (s.props.min && v < s.props.min) { 
                    v = s.props.min;
                    e = String(v);
                } 
                if (s.props.max && v > s.props.max) { 
                    v = s.props.max;
                    e = String(v);
                } 
                s.setState({'error':false,'value':String(Math.trunc(v))});
                s.props.onChange(Math.trunc(v))
            }catch(ee){
                s.setState({'error':false,'value':s.state.lastDefault});
            }
        }""",
        },
    )
    return Component


def InputChoice():
    name = "InputChoice"
    form = TeleportElement(MaterialContent(elementType="FormControl"))
    form.content.attrs["fullWidth"] = True
    form.content.attrs["variant"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "variant"},
    }
    label = TeleportElement(MaterialContent(elementType="InputLabel"))
    label.content.attrs["htmlFor"] = "component-filled"
    label.content.attrs["shrink"] = True
    label.content.style = {"background": "white", "padding": "0px 2px", "left": "-5px"}
    labeltext = TeleportDynamic(content={"referenceType": "prop", "id": "label"})

    helpertext = TeleportElement(MaterialContent(elementType="FormHelperText"))
    helpertext.addContent(
        TeleportDynamic(content={"referenceType": "prop", "id": "description"})
    )
    label.addContent(labeltext)
    string = TeleportElement(MaterialContent(elementType="Select"))
    string.content.attrs["select"] = True
    string.content.attrs["fullWidth"] = True
    string.content.style = {"margin": "10px 0px 10px 0px"}
    string.content.attrs[
        "dummy"
    ] = "$self.props.onDefault(self, self.props.value)"
    string.content.attrs["value"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "value"},
    }
    string.content.attrs["suffix"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "suffix"},
    }
    string.content.events["change"] = []
    string.content.events["change"].append(
        {"type": "propCall2", "calls": "onValidate", "args": ["self", "e.target.value"]}
    )
    string.content.attrs["disabled"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "disabled"},
    }
    option = TeleportElement(MaterialContent(elementType="MenuItem"))
    option.content.attrs["key"] = {
        "type": "dynamic",
        "content": {"referenceType": "local", "id": "local"},
    }
    option.content.attrs["value"] = {
        "type": "dynamic",
        "content": {"referenceType": "local", "id": "local"},
    }
    option.content.style = {"width": "100%"}
    option.addContent(TeleportStatic(content="$local"))
    options = TeleportRepeat(option)
    options.iteratorName = "local"
    options.dataSource = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "options"},
    }
    string.addContent(options)
    form.addContent(label)
    form.addContent(string)
    form.addContent(helpertext)
    
    Component = TeleportComponent(name, form)
    Component.addStateVariable(
        "value", {"type": "string", "defaultValue": "$self.props.value"}
    )
    Component.addStateVariable(
        "lastDefault", {"type": "string", "defaultValue": "$self.props.value"}
    )
    Component.addPropVariable("variant", {"type": "string", "defaultValue": "outlined"})
    Component.addPropVariable("label", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("disabled", {"type": "boolean", "defaultValue": False})
    Component.addPropVariable("description", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("options", {"type": "array", "defaultValue": []})
    Component.addPropVariable("value", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("onChange", {"type": "func", "defaultValue": "(e)=>{}"})
    Component.addPropVariable(
        "onDefault",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            let a = e; 
            if (s.state && a!=s.state.lastDefault)
                s.setState({'lastDefault':a,'value':a});
            return a;
        }""",
        },
    )

    Component.addPropVariable(
        "onValidate",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            s.props.onChange(e)
        }""",
        },
    )

    return Component


def InputText():
    name = "InputText"
    string = TeleportElement(MaterialContent(elementType="TextField"))
    string.content.attrs["variant"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "variant"},
    }
    string.content.attrs["label"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "label"},
    }
    string.content.attrs["fullWidth"] = True
    string.content.attrs["helperText"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "description"},
    }
    string.content.attrs["multiline"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "multiline"},
    }
    string.content.style = {"margin": "10px 0px 10px 0px"}
    string.content.attrs[
        "dummy"
    ] = "$self.props.onDefault(self, self.props.value)"
    string.content.attrs["value"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "value"},
    }
    string.content.attrs["suffix"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "suffix"},
    }
    string.content.events["change"] = []
    string.content.events["change"].append(
        {"type": "propCall2", "calls": "onValidate", "args": ["self", "e.target.value"]}
    )
    string.content.attrs["disabled"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "disabled"},
    }
    Component = TeleportComponent(name, string)
    Component.addStateVariable(
        "value", {"type": "string", "defaultValue": "$self.props.value"}
    )
    Component.addStateVariable(
        "lastDefault", {"type": "string", "defaultValue": "$self.props.value"}
    )

    Component.addPropVariable("variant", {"type": "string", "defaultValue": "outlined"})
    Component.addPropVariable("multiline", {"type": "boolean", "defaultValue": False})
    Component.addPropVariable("suffix", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("disabled", {"type": "boolean", "defaultValue": False})
    Component.addPropVariable("label", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("description", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("value", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("onChange", {"type": "func", "defaultValue": "(e)=>{}"})
    Component.addPropVariable(
        "onDefault",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            let a = e; 
            if (s.state && a!=s.state.lastDefault)
                s.setState({'lastDefault':a,'value':a});
            return a;
        }""",
        },
    )

    Component.addPropVariable(
        "onValidate",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            s.props.onChange(e)
        }""",
        },
    )

    return Component


def InputBoolean():
    name = "InputBoolean"
    form = TeleportElement(MaterialContent(elementType="FormControl"))
    form.content.attrs["fullWidth"] = True
    form.content.attrs["variant"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "variant"},
    }
    form.content.style = {
        "border": "1px solid rgba(0, 0, 0, 0.23)",
        "borderRadius": "4px",
        "flexDirection": "row",
        "width": "100%",
    }
    label = TeleportElement(MaterialContent(elementType="InputLabel"))
    label.content.attrs["htmlFor"] = "component-filled"
    label.content.attrs["shrink"] = True
    label.content.style = {
        "background": "white",
        "padding": "0px 2px",
        "left": "-5px",
        "top": "-5px",
    }
    labeltext = TeleportDynamic(content={"referenceType": "prop", "id": "label"})

    helpertext = TeleportElement(MaterialContent(elementType="FormHelperText"))
    helpertext.addContent(
        TeleportDynamic(content={"referenceType": "prop", "id": "description"})
    )
    label.addContent(labeltext)

    string = TeleportElement(MaterialContent(elementType="Switch"))

    string.content.attrs["fullWidth"] = True
    string.content.attrs["disabled"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "disabled"},
    }
    string.content.attrs[
        "dummy"
    ] = "$self.props.onDefault(self, self.props.value)"
    string.content.attrs["checked"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "value"},
    }
    string.content.events["change"] = []
    string.content.events["change"].append(
        {
            "type": "propCall2",
            "calls": "onValidate",
            "args": ["self", "e.target.checked"],
        }
    )

    form.addContent(label)
    form.addContent(string)
    form.addContent(helpertext)
    Component = TeleportComponent(name, form)

    Component.addStateVariable(
        "value", {"type": "string", "defaultValue": "$self.props.value"}
    )
    Component.addStateVariable(
        "lastDefault", {"type": "string", "defaultValue": "$self.props.value"}
    )

    Component.addPropVariable("variant", {"type": "string", "defaultValue": "outlined"})
    Component.addPropVariable("label", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("description", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("disabled", {"type": "boolean", "defaultValue": False})
    Component.addPropVariable("value", {"type": "boolean", "defaultValue": False})
    Component.addPropVariable("onChange", {"type": "func", "defaultValue": "(e)=>{}"})
    Component.addPropVariable(
        "onDefault",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            let a = e; 
            if (s.state && a!=s.state.lastDefault)
                s.setState({'lastDefault':a,'value':a});
            return a;
        }""",
        },
    )

    Component.addPropVariable(
        "onValidate",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            s.props.onChange(e)
        }""",
        },
    )

    return Component

def InputFile():
    name = "InputFile"
    
    container = TeleportElement(MaterialContent(elementType="FormControl"))
    container.content.attrs["fullWidth"] = True

    form = TeleportElement(MaterialContent(elementType="FormControl"))
    form.content.attrs["fullWidth"] = True
    form.content.attrs["variant"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "variant"},
    }
    form.content.style = {
        "border": "1px solid rgba(0, 0, 0, 0.23)",
        "borderRadius": "4px",
        "flexDirection": "row",
        "width": "100%",
        "padding" : "5px"
    }
    label = TeleportElement(MaterialContent(elementType="InputLabel"))
    label.content.attrs["htmlFor"] = "component-filled"
    label.content.attrs["shrink"] = True
    label.content.style = {"background": "white", "padding": "0px 2px", "left": "-5px"}
    labeltext = TeleportDynamic(content={"referenceType": "prop", "id": "label"})

    helpertext = TeleportElement(MaterialContent(elementType="FormHelperText"))
    helpertext.addContent(
        TeleportDynamic(content={"referenceType": "prop", "id": "description"})
    )
    helpertext.content.style = {
        "marginLeft" : "14px"
    }
    label.addContent(labeltext)
    
    string = TeleportElement(MaterialContent(elementType="Button"))
    inputs = TeleportElement(TeleportContent(elementType="input"))
    inputs.content.attrs["type"] = "file"
    inputs.content.attrs["accept"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "accept"},
    }
    inputs.content.attrs["hidden"] = True
    inputs.content.style = {'display': 'none'}
    label1 = TeleportStatic(content="Upload File [")
    label2 = TeleportDynamic(content={
        "referenceType": "state",
        "id": "filename"
    })
    label3 = TeleportStatic(content="]")
    icon = TeleportElement(MaterialContent(elementType="Icon"))
    icontext = TeleportStatic(content="file_upload")
    string.content.attrs["component"] = "label"
    string.content.attrs["disabled"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "disabled"},
    }
    string.content.attrs["fullWidth"] = True
    string.content.events["change"] = []
    string.content.events["change"].append({
        "type": "propCall2",
        "calls": "onValidate",
        "args": ["self", "e.target.files"],
    })
    icon.addContent(icontext)
    string.addContent(icon)
    string.addContent(label1)
    string.addContent(label2)
    string.addContent(label3)
    string.addContent(inputs)

    form.addContent(label)
    form.addContent(string)
    container.addContent(form)
    container.addContent(helpertext)
    Component = TeleportComponent(name, container)
    
    Component.addStateVariable("filename", {
        "type": "string",
        "defaultValue": ""
    })
    Component.addStateVariable("error", {
        "type": "boolean",
        "defaultValue": False
    })
    Component.addPropVariable("variant", {
        "type": "string",
        "defaultValue": "outlined"
    })
    Component.addPropVariable("label", {
        "type": "string", 
        "defaultValue": ""
    })
    Component.addPropVariable("accept", {
        "type": "string", 
        "defaultValue": "*"
    })
    Component.addPropVariable("description", {
        "type": "string",
        "defaultValue": ""
    })
    Component.addPropVariable("value", {
        "type": "boolean",
        "defaultValue": False
    })
    Component.addPropVariable("onChange", {
        "type": "func",
        "defaultValue": "(e)=>{}"
    })
    Component.addPropVariable("disabled", {"type": "boolean", "defaultValue": False})
    Component.addPropVariable(
        "onValidate",
        {
            "type":
            "func",
            "defaultValue":
            """(s,e)=>{
            if (!e) {
              return;
            }
            let file = e[0];
            const reader = new FileReader();
            reader.onload = (evt) => {
              try{
                if (!evt?.target?.result) {
                  return;
                }
                const { result } = evt.target;
                var binary = '';
                var bytes = new Uint8Array( result );
                var len = bytes.byteLength;
                for (var i = 0; i < len; i++) {
                  binary += String.fromCharCode( bytes[ i ] );
                }
                let bt =  window.btoa( binary );
                s.setState({'error':false, 'filename':file.name})
                s.props.onChange("base64://"+bt)
              } catch {
                s.setState({'error':true, 'filename':''})
              }
            };
            reader.readAsArrayBuffer(file);
        }""",
        },
    )

    return Component



def Loader(Component, *args, **kwargs):
    Component.addStateVariable(
        kwargs.get("loader_status", "loader_status"),
        {"type": "string", "defaultValue": ""},
    )
    Component.addStateVariable(
        kwargs.get("loader_open", "loader_open"),
        {"type": "boolean", "defaultValue": kwargs.get("is_open", True)},
    )

    Loader = TeleportElement(MaterialContent(elementType="Dialog"))
    Loader.content.attrs["open"] = {
        "type": "dynamic",
        "content": {
            "referenceType": "state",
            "id": kwargs.get("open", "loader_open"),
        },
    }
    #Loader.content.attrs["disableBackdropClick"] = True
    Loader.content.attrs["disableEscapeKeyDown"] = True
    Loader.content.attrs["fullWidth"] = True
    Loader.content.attrs["maxWidth"] = "xs"
    loadercnt = TeleportElement(MaterialContent(elementType="DialogContent"))
    loadercnt.content.style = {"textAlign": "center", "overflow": "hidden"}

    LinearProgress = TeleportElement(MaterialContent(elementType="LinearProgress"))
    LinearProgress.content.attrs["color"] = "secondary"

    loadertext = TeleportElement(MaterialContent(elementType="DialogTitle"))
    loadertext.addContent(
        TeleportDynamic(
            content={
                "referenceType": "state",
                "id": kwargs.get("open", "loader_status"),
            }
        )
    )
    loadertext.content.style = {"textAlign": "center"}

    # loadercnt.addContent(loadercir)
    loadercnt.addContent(LinearProgress)
    Loader.addContent(loadercnt)
    Loader.addContent(loadertext)

    return Loader

def Error(Component, *args, **kwargs):
    Component.addStateVariable(
        kwargs.get("error_status", "error_status"),
        {"type": "string", "defaultValue": ""},
    )
    Component.addStateVariable(
        kwargs.get("error_open", "error_open"),
        {"type": "boolean", "defaultValue": False},
    )
    Error = TeleportElement(MaterialContent(elementType="Dialog"))
    Error.content.attrs["open"] = {
        "type": "dynamic",
        "content": {
            "referenceType": "state",
            "id": kwargs.get("error_open", "error_open"),
        },
    }
    Error.content.attrs["fullWidth"] = True
    Error.content.attrs["maxWidth"] = "xs"
    DialogContent = TeleportElement(MaterialContent(elementType="DialogContent"))
    DialogContent.content.style = {"textAlign": "center", "overflow": "hidden"}

    Typography = TeleportElement(MaterialContent(elementType="Typography"))
    Typography.content.attrs["variant"] = "h6"
    TypographyText = TeleportStatic(content=kwargs.get("title", "Error Message"))
    Typography.addContent(TypographyText)

    Icon0 = TeleportElement(MaterialContent(elementType="Icon"))
    Icon0.content.style = {"position": "absolute", "top": "10px", "left": "10px"}
    IconText0 = TeleportStatic(content="error")
    Icon0.addContent(IconText0)

    IconButton = TeleportElement(MaterialContent(elementType="IconButton"))
    IconButton.content.style = {
        "position": "absolute",
        "top": "10px",
        "right": "10px",
    }

    Icon = TeleportElement(MaterialContent(elementType="Icon"))
    IconText = TeleportStatic(content="close")
    Icon.addContent(IconText)
    IconButton.addContent(Icon)
    IconButton.content.events["click"] = [
        {
            "type": "stateChange",
            "modifies": kwargs.get("error_open", "error_open"),
            "newState": False,
        }
    ]

    DialogTitle = TeleportElement(MaterialContent(elementType="DialogTitle"))
    DialogTitle.content.attrs["disableTypography"] = True
    DialogTitle.content.style = {
        "textAlign": "center",
        "backgroundColor": "#d95c5c",
    }
    DialogTitle.addContent(IconButton)
    DialogTitle.addContent(Typography)
    DialogTitle.addContent(Icon0)

    DialogContent.addContent(
        TeleportDynamic(
            content={
                "referenceType": "state",
                "id": kwargs.get("error_status", "error_status"),
            }
        )
    )
    DialogContent.content.style = {"textAlign": "center"}

    Error.addContent(DialogTitle)
    Error.addContent(DialogContent)
    return Error

def AppBar(*args, **kwargs):
    AppBar = TeleportElement(MaterialContent(elementType="AppBar"))
    AppBar.content.attrs["position"] = "static"
    AppBar.content.attrs["color"] = kwargs.get("color", "primary")
    AppBar.content.style = {"width": "inherit"}

    ToolBar = TeleportElement(MaterialContent(elementType="Toolbar"))
    ToolBar.content.attrs["variant"] = kwargs.get("variant", "regular")

    Typography = TeleportElement(MaterialContent(elementType="Typography"))
    Typography.content.attrs["variant"] = "h6"
    Typography.content.style = {"flex": 1, "textAlign": "center"}
    TypographyText = TeleportStatic(content=kwargs.get("title", ""))
    Typography.addContent(TypographyText)
    
    ToolBar.addContent(Typography)
    AppBar.addContent(ToolBar)
    return AppBar


def Results(*args, **kwargs):
    results = kwargs.get("results", {})
    onClick = kwargs.get("onClick", [])
    onLoad = kwargs.get("onLoad", [])
    ToggleButtonGroup = TeleportElement(
        MaterialContent(elementType="ToggleButtonGroup")
    )
    ToggleButtonGroup.content.style = {
        "width": "100%",
        "flexDirection": "column",
        "display": "inline-flex",
    }
    ToggleButtonGroup.content.attrs["orientation"] = "vertical"
    ToggleButtonGroup.content.attrs["exclusive"] = True

    ToggleButtonGroup.content.attrs["value"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "open_plot"},
    }

    for k, v in results.items():
        v_action = []
        if isinstance(v["action"], dict):
            v_action.append(v["action"])
        elif isinstance(v["action"], list):
            for va in v["action"]:
                v_action.append(va)
        v_action.append(
            {"type": "stateChange", "modifies": "open_plot", "newState": k}
        )
        ToggleButton = TeleportElement(
            MaterialContent(elementType="ToggleButton")
        )
        ToggleButton.content.attrs["value"] = k
        ToggleButton.content.events["click"] = onClick + v_action + onLoad
        Typography = TeleportElement(MaterialContent(elementType="Typography"))
        Typography.addContent(TeleportStatic(content=v["title"]))
        ToggleButton.addContent(Typography)
        ToggleButtonGroup.addContent(ToggleButton)

    return ToggleButtonGroup