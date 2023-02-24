import nanohubuidl.teleport as t
import nanohubuidl.material as m

def InputDict():
    name = "InputDict"
    string = t.TeleportElement(m.MaterialContent(elementType="TextField"))
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
        "defaultValue"
    ] = "$self.props.onDefault(self, self.props.value)"
    string.content.attrs["value"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "value"},
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

    Component = t.TeleportComponent(name, string)

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
    string = t.TeleportElement(m.MaterialContent(elementType="TextField"))
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
        "defaultValue"
    ] = "$self.props.onDefault(self, self.props.value)"
    string.content.attrs["value"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "value"},
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

    Component = t.TeleportComponent(name, string)

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
    string = t.TeleportElement(m.MaterialContent(elementType="TextField"))
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
        "defaultValue"
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

    string.content.attrs["error"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "error"},
    }

    Component = t.TeleportComponent(name, string)

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
    string = t.TeleportElement(m.MaterialContent(elementType="TextField"))
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
        "defaultValue"
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

    string.content.attrs["error"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "error"},
    }

    Component = t.TeleportComponent(name, string)

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
    form = t.TeleportElement(m.MaterialContent(elementType="FormControl"))
    form.content.attrs["fullWidth"] = True
    form.content.attrs["variant"] = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "variant"},
    }
    label = t.TeleportElement(m.MaterialContent(elementType="InputLabel"))
    label.content.attrs["htmlFor"] = "component-filled"
    label.content.attrs["shrink"] = True
    label.content.style = {"background": "white", "padding": "0px 2px", "left": "-5px"}
    labeltext = t.TeleportDynamic(content={"referenceType": "prop", "id": "label"})

    helpertext = t.TeleportElement(m.MaterialContent(elementType="FormHelperText"))
    helpertext.addContent(
        t.TeleportDynamic(content={"referenceType": "prop", "id": "description"})
    )
    label.addContent(helpertext)
    string = t.TeleportElement(m.MaterialContent(elementType="Select"))
    string.content.attrs["select"] = True
    string.content.attrs["fullWidth"] = True
    string.content.style = {"margin": "10px 0px 10px 0px"}
    string.content.attrs[
        "defaultValue"
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
    option = t.TeleportElement(m.MaterialContent(elementType="MenuItem"))
    option.content.attrs["key"] = {
        "type": "dynamic",
        "content": {"referenceType": "local", "id": "local"},
    }
    option.content.attrs["value"] = {
        "type": "dynamic",
        "content": {"referenceType": "local", "id": "local"},
    }
    option.content.style = {"width": "100%"}
    option.addContent(t.TeleportStatic(content="$local"))
    options = t.TeleportRepeat(option)
    options.iteratorName = "local"
    options.dataSource = {
        "type": "dynamic",
        "content": {"referenceType": "prop", "id": "options"},
    }
    string.addContent(options)
    form.addContent(label)
    form.addContent(string)
    form.addContent(helpertext)
    
    Component = t.TeleportComponent(name, form)
    Component.addStateVariable(
        "value", {"type": "string", "defaultValue": "self.props.value"}
    )
    Component.addStateVariable(
        "lastDefault", {"type": "string", "defaultValue": "self.props.value"}
    )
    Component.addPropVariable("variant", {"type": "string", "defaultValue": "outlined"})
    Component.addPropVariable("label", {"type": "string", "defaultValue": ""})
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
    string = t.TeleportElement(m.MaterialContent(elementType="TextField"))
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
        "defaultValue"
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
    Component = t.TeleportComponent(name, string)
    Component.addStateVariable(
        "value", {"type": "string", "defaultValue": "self.props.value"}
    )
    Component.addStateVariable(
        "lastDefault", {"type": "string", "defaultValue": "self.props.value"}
    )

    Component.addPropVariable("variant", {"type": "string", "defaultValue": "outlined"})
    Component.addPropVariable("multiline", {"type": "boolean", "defaultValue": False})
    Component.addPropVariable("suffix", {"type": "string", "defaultValue": ""})
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
    form = t.TeleportElement(m.MaterialContent(elementType="FormControl"))
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
    label = t.TeleportElement(m.MaterialContent(elementType="InputLabel"))
    label.content.attrs["htmlFor"] = "component-filled"
    label.content.attrs["shrink"] = True
    label.content.style = {
        "background": "white",
        "padding": "0px 2px",
        "left": "-5px",
        "top": "-5px",
    }
    labeltext = t.TeleportDynamic(content={"referenceType": "prop", "id": "label"})

    helpertext = t.TeleportElement(m.MaterialContent(elementType="FormHelperText"))
    helpertext.addContent(
        t.TeleportDynamic(content={"referenceType": "prop", "id": "description"})
    )
    label.addContent(helpertext)

    string = t.TeleportElement(m.MaterialContent(elementType="Switch"))

    string.content.attrs["fullWidth"] = True

    string.content.attrs[
        "defaultValue"
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
    Component = t.TeleportComponent(name, form)

    Component.addStateVariable(
        "value", {"type": "string", "defaultValue": "self.props.value"}
    )
    Component.addStateVariable(
        "lastDefault", {"type": "string", "defaultValue": "self.props.value"}
    )

    Component.addPropVariable("variant", {"type": "string", "defaultValue": "outlined"})
    Component.addPropVariable("label", {"type": "string", "defaultValue": ""})
    Component.addPropVariable("description", {"type": "string", "defaultValue": ""})
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
