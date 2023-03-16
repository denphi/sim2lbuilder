import re
import nanohubuidl.app as a
import json
from nanohubuidl.teleport import TeleportComponent, TeleportElement, TeleportContent
from nanohubuidl.teleport import TeleportStatic, TeleportRepeat, TeleportDynamic
from nanohubuidl.teleport import NanohubUtils
from nanohubuidl.material import MaterialContent

eol = "\n"

def deleteHistory(tp, tc, *args, **kwargs):   
    eol = "\n";
    cache_store = kwargs.get("cache_store", "CacheStore");
    cache_storage = kwargs.get("cache_storage", "cacheFactory('"+cache_store+"', 'INDEXEDDB')")
    NanohubUtils.storageFactory(tp, store_name=cache_store, storage_name=cache_storage)          

    regc = tp.project_name    
    regc = "_" + re.sub("[^a-zA-Z0-9]+", "", regc) + "_"

    js = "async (component)=>{" + eol    
    js += "  let selfr = component;" + eol
    js += "  var listState = [];" + eol
    js += "  var activeCache = [];" + eol
    js += "  var olen = await " + cache_store + ".length();" + eol
    js += "  for (let ii=0; ii<olen; ii++) {" + eol
    js += "    var key = await " + cache_store + ".key(ii);" + eol
    js += "    const regex = new RegExp('" + regc + "([a-z0-9]{64})', 'im');" + eol
    js += "    let m;" + eol
    js += "    if ((m = regex.exec(key)) !== null) {" + eol
    js += "        if (component.state.lastCache != m[1]){ " + eol
    js += "            var deleted = await " + cache_store + ".removeItem(m[1]);" + eol
    js += "        }" + eol
    js += "    };" + eol
    js += "  }" 
    js += "  selfr.setState({'compare':false});" + eol
    js += "  selfr.props.refreshViews(selfr);" + eol

    js += "}" + eol
    tc.addPropVariable("deleteHistory", {"type":"func", 'defaultValue' :js})   

    return [
      {
        "type": "propCall2",
        "calls": "deleteHistory",
        "args": ['self', '']
      }
    ] 

def cleanCache(tp, tc, *args, **kwargs):   
    eol = "\n";
    cache_store = kwargs.get("cache_store", "CacheStore");
    store_name  = kwargs.get("store_name", "sessionStore");
    NanohubUtils.storageFactory(tp, store_name=store_name)
    
    js = "async (component)=>{" + eol    
    js += "  let selfr = component;" + eol
    js += "  var listState = [];" + eol
    js += "  var activeCache = [];" + eol
    js += "  let deleted = await " + cache_store + ".clear();" + eol
    js += "  deleted = await " + store_name + ".clear();" + eol
    js += "  selfr.props.onSuccess(component,'');" + eol
    
    js += "}" + eol
    tc.addPropVariable("cleanCache", {"type":"func", 'defaultValue' :js})   

    return [
      {
        "type": "propCall2",
        "calls": "cleanCache",
        "args": ['self', '']
      }
    ] 


def loadDefaultSimulation(tp, tc, *args, **kwargs):
    store_name="sessionStore";
    NanohubUtils.storageFactory(tp, store_name=store_name)
    eol = "\n"
    js = ""
    js += "async (self) => {" + eol
    js += "  if (self.state.default_loaded == false){" + eol
    js += "    self.state.default_loaded = true;" + eol
    js += "    if (" + store_name + ".getItem('nanohub_token')){" + eol
    js += "      self.props.onClick(self);" + eol
    js += "      self.props.onStatusChange({'target':{'value':'Loading Default Results'}});" + eol
    js += "      self.props.onSimulate(self);" + eol
    js += "    } else {" + eol
    js += "      setTimeout((s=self) => {" + eol
    js += "        if (" + store_name + ".getItem('nanohub_token')){" + eol
    js += "          s.props.onClick(self);" + eol
    js += "          s.props.onStatusChange({'target':{'value':'Loading Default Results'}});" + eol
    js += "          s.props.onSimulate(s);" + eol
    js += "        }" + eol
    js += "      }, 1500)" + eol
    js += "    } " + eol
    js += "  } " + eol
    js += "}" + eol
    tc.addPropVariable("onLoad", {"type":"func", "defaultValue": js})    
    tc.addStateVariable("default_loaded", {"type":"boolean", "defaultValue": False})    
    
    
def buildParams(inputs):
    params = {}
    parameters = {}
    Component = TeleportComponent("Dummy", TeleportElement(TeleportContent(elementType="container")))
    for k, v in inputs.items():
        if isinstance(k, str) == False or k.isnumeric():
            k = "_" + k
        if "type" in v:
            param = None
            value = {
                "type": "dynamic",
                "content": {"referenceType": "prop", "id": "parameters." + k},
            }
            if v["type"] == "input.Choice":
                param = TeleportElement(TeleportContent(elementType="InputChoice"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["options"] = v.get("options", [])
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Integer":
                param = TeleportElement(TeleportContent(elementType="InputInteger"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["suffix"] = v.get("units", "")
                param.content.attrs["min"] = v.get("min", None)
                param.content.attrs["max"] = v.get("max", None)
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Number":
                param = TeleportElement(TeleportContent(elementType="InputNumber"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["suffix"] = v.get("units", "")
                param.content.attrs["min"] = v.get("min", None)
                param.content.attrs["max"] = v.get("max", None)
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Text" :
                param = TeleportElement(TeleportContent(elementType="InputText"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["suffix"] = v.get("units", "")
                param.content.attrs["multiline"] = v.get("multiline", True)
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Tag" :
                param = TeleportElement(TeleportContent(elementType="InputText"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Boolean":
                param = TeleportElement(TeleportContent(elementType="InputBoolean"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Dict":
                param = TeleportElement(TeleportContent(elementType="InputDict"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.List" or v["type"] == "input.Array":
                param = TeleportElement(TeleportContent(elementType="InputList"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.File":
                param = TeleportElement(TeleportContent(elementType="InputFile"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["accept"] = v.get("accept", "*")
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Image":
                param = TeleportElement(TeleportContent(elementType="InputFile"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["accept"] = v.get("accept", "image/*")
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Element":
                print(v["type"] + "is not supported");

            if param is not None:
                params[k] = param
            
    return params

def buildLayout(layout):
    lay = {}
    if layout["type"] == "VBox":
        lay["type"] = "group"
        lay["layout"] = "vertical"
    elif layout["type"] == "HBox":
        lay["type"] = "group"
        lay["layout"] = "horizontal"
    elif layout["type"] == "Box":
        lay["type"] = "group"
    elif layout["type"] == "Tab":
        lay["type"] = "tab"
    lay["label"] = layout.get("label", "")
    lay["children"] = []
    for c in layout["children"]:
        if isinstance(c, dict) == True:
            lay["children"].append(buildLayout(c))
        elif isinstance(c, str) == True and c.startswith("input."):
            lay["children"].append({'type': 'number', 'id': c.replace("input.", ""), 'label': '', 'enable': None})
        else:
            lay["children"].append(c)
    return lay


def Settings(tp, Component, *args, **kwargs):
    outputs = kwargs.get("outputs", [])
    params = kwargs.get("params", {})
    layout = kwargs.get("layout", {})
    url = kwargs.get("url", "")
    revision = kwargs.get("revision", "")
    toolname = kwargs.get("toolname", "")
    parameters = kwargs.get("parameters", {})
    
    NComponent = TeleportComponent(
        "AppSettingsComponent",
        TeleportElement(MaterialContent(elementType="Paper")),
    )
    deffunc = {"type": "func", "defaultValue": "(e)=>{}"}
    NComponent.node.content.style = {"width": "100%"}
    NComponent.addPropVariable("onSubmit", deffunc)
    NComponent.addPropVariable("onClick", deffunc)
    NComponent.addPropVariable("onChange", deffunc)
    NComponent.addPropVariable("onLoad", deffunc)
    NComponent.addPropVariable("onSuccess", deffunc)
    NComponent.addPropVariable("onError", deffunc)
    NComponent.addPropVariable("onStatusChange",deffunc)
    NComponent.addPropVariable("parameters", {"type": "object", "defaultValue": {}})
    NComponent.addStateVariable(
        "lastDefault",
        {"type": "string", "defaultValue": "$JSON.stringify(self.props.parameters)"},
    )
    NComponent.addPropVariable(
        "onDefault",
        {
            "type": "func",
            "defaultValue": """(s,e)=>{
            let a = JSON.stringify(e); 
            if (s.state && a!=s.state.lastDefault)
                s.setState({'lastDefault':a, ...e});
            return e;
        }""",
        },
    )
    
    Tabs = a.AppBuilder.createGroups(NComponent, layout, params)
    
    runSimulation = onSimulate(
        tp,
        NComponent,
        cache_store=kwargs.get("cache_store", "CacheStore"),
        toolname=toolname,
        revision=revision,
        url=url,
        outputs=outputs,
        jupyter_cache=None,
        delay = kwargs.get("delay", 5000)
    )

    runSimulation.append(
        {
            "type": "propCall2",
            "calls": "onClick",
            "args": [runSimulation[0]["args"][1]],
        }
    )
    runSimulation.append(
        {
            "type": "propCall2",
            "calls": "onSubmit",
            "args": [runSimulation[0]["args"][1]],
        }
    )
    Grid = TeleportElement(MaterialContent(elementType="Grid"))
    Grid.content.attrs["container"] = True
    Grid.content.attrs["direction"] = "column"
    Grid.content.attrs["dummy"] = "$self.props.onDefault(self, self.props.parameters)"
        
    Text0 = TeleportStatic()
    Text0.content = "Simulate"
    ToggleButton0 = TeleportElement(MaterialContent(elementType="ToggleButton"))
    ToggleButton0.addContent(Text0)
    ToggleButton0.content.attrs["selected"] = True
    ToggleButton0.content.style = {"width":"inherit"}
    ToggleButton0.content.events['click'] = runSimulation
    ToggleButton0.content.attrs["value"] = "runSimulation"

    ToggleButton1 = TeleportElement(MaterialContent(elementType="ToggleButton"))
    ToggleButton1.addContent(Text0)
    ToggleButton1.content.attrs["selected"] = True
    ToggleButton1.content.style = {"width":"inherit"}
    ToggleButton1.content.events['click'] = runSimulation
    ToggleButton1.content.attrs["value"] = "runSimulation"

    
    Tabs.addContent(Grid)

    Gridt = TeleportElement(MaterialContent(elementType="Grid"))
    Gridt.content.attrs["color"] = "secondary"
    Gridt.content.attrs["container"] = True
    Gridt.content.attrs["direction"] = "column"
    resetv = []
    resetv = [{ "type": "stateChange", "modifies": k,"newState": v}
        for k,v in parameters.items()
    ]
    resetv.append({
        'type': 'propCall2',
        'calls': 'onChange',
        'args': [json.dumps(parameters)]
    })

    Buttontt = TeleportElement(MaterialContent(elementType="ToggleButton"))
    Buttontt.addContent(TeleportStatic(content="Restore Default Parameters"))
    Buttontt.content.attrs["selected"] = True
    Buttontt.content.attrs["value"] = "Restore"
    Buttontt.content.style = {
        'backgroundColor':'#999999', 
        'color':'rgba(255, 255, 255, 0.87)',
        'width':'inherit'
    }
    Buttontt.content.events['click'] = resetv

    onCleanCache = cleanCache(tp, NComponent)  

    Buttontc = TeleportElement(MaterialContent(elementType="ToggleButton"))
    Buttontc.addContent(TeleportStatic(content="Purge Cached Results"))
    Buttontc.content.attrs["selected"] = True
    Buttontc.content.style = {
        'backgroundColor':'#990000', 
        'color':'rgba(255, 255, 255, 0.87)',
        'width':'inherit'
    }
    Buttontc.content.events['click'] = onCleanCache
    Buttontc.content.attrs["value"] = "onCleanCache"


    NComponent.node.addContent(ToggleButton0)
    NComponent.node.addContent(Tabs)
    NComponent.node.addContent(ToggleButton1)
    NComponent.node.addContent(Buttontt)
    NComponent.node.addContent(Buttontc)

    NComponent.addPropVariable(
        "parameters", {"type": "object", "defaultValue": parameters}
    )

    return NComponent

def onSimulate(tp, Component, *args, **kwargs):
    buildSchema(tp, Component, *args, **kwargs)
    store_name = "sessionStore"
    NanohubUtils.storageFactory(
        tp, store_name=store_name, storage_name="window.sessionStorage"
    )
    use_cache = kwargs.get("use_cache", True)
    delay = kwargs.get("delay", 5000)
    outputs = kwargs.get("outputs", [])
    if use_cache:
        cache_store = kwargs.get("cache_store", "CacheStore")
        if kwargs.get("jupyter_cache", None) is not None:
            cache_storage = kwargs.get(
                "cache_storage",
                "cacheFactory('" + cache_store + "', 'JUPYTERSTORAGE')",
            )
            NanohubUtils.storageFactory(
                tp,
                method_name="storageJupyterFactory",
                jupyter_cache=kwargs.get("jupyter_cache", None),
                store_name=cache_store,
                storage_name=cache_storage,
            )
        else:
            cache_storage = kwargs.get(
                "cache_storage", "cacheFactory('" + cache_store + "', 'INDEXEDDB')"
            )
            NanohubUtils.storageFactory(
                tp, store_name=cache_store, storage_name=cache_storage
            )
    eol = "\n"
    toolname = kwargs.get("toolname", "")
    revision = kwargs.get("revision", "")
    url = kwargs.get("url", "")

    js = "async (self, ostate)=>{" + eol
    js += "  var state = self.state;" + eol

    if use_cache:
        js += (
            "  self.props.onStatusChange({'target':{ 'value' : 'Checking Cache' } } );"
            + eol
        )
        js += "  var d_state = Object.assign({}, self.state);" + eol
        js += "  delete d_state['testing'];" + eol
        js += "  var str_key = JSON.stringify(d_state);" + eol
        js += "  var buffer_key = new TextEncoder('utf-8').encode(str_key);" + eol
        js += (
            "  var hashBuffer = await window.crypto.subtle.digest('SHA-256', buffer_key);"
            + eol
        )
        js += "  var hashArray = Array.from(new Uint8Array(hashBuffer));" + eol
        js += (
            "  var hash_key = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');"
            + eol
        )
        # js += "  console.log(hash_key)" + eol
        js += "  var hash_q = await " + cache_store + ".getItem(hash_key)" + eol
        # js += "  console.log(hash_q)" + eol
        js += "  if( hash_q == null ){" + eol
    js += (
        "  self.props.onStatusChange({'target':{ 'value' : 'Parsing Tool Schema' } } );"
        + eol
    )
    js += (
        "  var schema = JSON.parse("
        + store_name
        + ".getItem('nanohub_tool_schema'));"
        + eol
    )
    js += "  if(!schema){" + eol
    js += "    await self.props.buildSchema(self);" + eol
    js += (
        "    schema = JSON.parse("
        + store_name
        + ".getItem('nanohub_tool_schema'));"
        + eol
    )
    js += "    if(!schema){" + eol
    js += (
        "      self.props.onError( 'Error submiting the simulation, schema can not be loaded' );"
        + eol
    )
    js += "      return;" + eol
    js += "    }" + eol
    js += "  }" + eol
    js += "  var inputs = {};" + eol
    js += "  for (const id in schema.inputs) {" + eol
    js += "    if (id in state){" + eol
    js += "      inputs[id] = state[id];" + eol
    js += "    } else {" + eol
    js += "      inputs[id] = schema.inputs[id].value;" + eol
    js += "    }" + eol
    js += "  }" + eol
    # js += "  console.log(inputs);" + eol
    js += "  let data = {" + eol
    js += "    'name': '" + toolname + "', " + eol
    js += "    'revision': '" + str(revision) + "', " + eol
    js += "    'inputs': inputs, " + eol
    js += "    'outputs':" + json.dumps(outputs) + "," + eol
    js += "    'cores' : state['cores']," + eol
    js += "    'cutoff' : state['cutoff']," + eol
    js += "    'venue' : state['venue']" + eol
    js += "  }" + eol
    js += "  var nanohub_token = " + store_name + ".getItem('nanohub_token');" + eol
    js += "  var header_token = {'Authorization': 'Bearer ' + nanohub_token}" + eol
    js += "  var url = '" + url + "/run';" + eol
    js += (
        "  self.props.onStatusChange({'target':{ 'value' : 'Submitting Simulation' } } );"
        + eol
    )
    js += (
        "  var options = { 'handleAs' : 'json' , 'headers' : header_token, 'method' : 'POST', 'data' : data };"
        + eol
    )
    js += "  try{" + eol
    js += "    Axios.request(url, options)" + eol
    js += "    .then(function(response){" + eol
    js += "      var data = response.data;" + eol
    # js += "      console.log(data);" + eol
    js += "      if(data.code){" + eol
    js += "        if(data.message){" + eol
    js += (
        "          self.props.onError( '(' + data.code + ') ' +data.message );"
        + eol
    )
    js += "        } else {" + eol
    js += (
        "          self.props.onError( '(' + data.code + ') Error sending the simulation' );"
        + eol
    )
    js += "        } " + eol
    js += "      }else{" + eol
    js += "        if(data.id){" + eol
    js += "          if('outputs' in data){" + eol
    js += "            self.props.onLoad(self);" + eol
    js += (
        "            self.props.onLoadResults(self, data.id, data['outputs']);"
        + eol
    )
    js += "          } else {" + eol
    js += (
        "            setTimeout(function(){ self.props.onCheckSession(self, data.id, 10) }, "+str(delay)+");"
        + eol
    )
    js += "          }" + eol
    js += "        } else {" + eol
    js += (
        "          self.props.onError( 'Error submiting the simulation, session not found' );"
        + eol
    )
    js += "        }" + eol
    js += "      }" + eol
    js += "    }).catch(function(error){" + eol
    js += "      if (error.response){" + eol
    js += "        if (error.response.data){" + eol
    js += "          if (error.response.data.message){" + eol
    js += (
        "            self.props.onError(String(error.response.data.message));" + eol
    )
    js += "          } else {" + eol
    js += "            self.props.onError(String(error.response.data));" + eol
    js += "          }" + eol
    js += "        } else {" + eol
    js += "          self.props.onError(String(error.response));" + eol
    js += "        }" + eol
    js += "      } else {" + eol
    js += "        self.props.onError(String(error));" + eol
    js += "      }" + eol
    js += "    });" + eol
    js += "  } catch (err) {" + eol
    js += "    self.props.onError(String(err));" + eol
    js += "  }" + eol
    if use_cache:
        js += "  } else { " + eol
        js += (
            "    self.props.onStatusChange({'target':{ 'value' : 'Loading from local Cache' } } );"
            + eol
        )
        js += "    self.props.onSuccess(self, hash_key)" + eol
        js += "  }" + eol
    js += "}"

    Component.addPropVariable("onSimulate", {"type": "func", "defaultValue": js})

    js = "(self, session_id, reload)=>{" + eol
    js += "  if (session_id == ''){" + eol
    js += "     self.props.onError('invalid Session ID');" + eol
    js += "  }" + eol
    js += "  var session_json = {'session_num': session_id};" + eol
    js += "  var nanohub_token = " + store_name + ".getItem('nanohub_token');" + eol
    js += "  var header_token = {'Authorization': 'Bearer ' + nanohub_token}" + eol
    js += "  var url = '" + url + "/run/' + session_id;" + eol
    js += "  var str = [];" + eol
    js += "  for(var p in session_json){" + eol
    js += (
        "    str.push(encodeURIComponent(p) + '=' + encodeURIComponent(session_json[p]));"
        + eol
    )
    js += "  }" + eol
    js += "  let data =  str.join('&');" + eol
    js += (
        "  var options = { 'handleAs' : 'json' , 'headers' : header_token, 'method' : 'POST', 'data' : data };"
        + eol
    )
    js += "  try{" + eol
    js += "    Axios.request(url, options)" + eol
    js += "    .then(function(response){" + eol
    js += "      var status = response.data;" + eol
    js += "      if (status['success']){" + eol
    js += "        if ('status' in status){" + eol
    js += "          if(status['status'] == 'error'){" + eol
    js += "            self.props.onError(status['status']);" + eol
    js += "          }" + eol
    js += "          else {" + eol
    js += (
        "            self.props.onStatusChange({'target':{ 'value' : status['status'] } } );"
        + eol
    )
    js += "            if('outputs' in status && status['outputs']){" + eol
    js += "              self.props.onLoad(self);" + eol
    js += (
        "              self.props.onLoadResults(self, session_id, status['outputs']);"
        + eol
    )
    js += "            } else {" + eol
    js += "              if (reload > 0){" + eol
    js += (
        "                setTimeout(function(){self.props.onCheckSession(self, session_id, reload)},"+str(delay)+");"
        + eol
    )
    js += "              }" + eol
    js += "            }" + eol
    js += "          }" + eol
    js += "        }"
    js += "      } else if (status['code']){" + eol
    js += "          self.props.onError(status['message']);" + eol
    js += "      }"
    js += "    }).catch(function(error){" + eol
    js += "      if (error.response){" + eol
    js += "        if (error.response.data){" + eol
    js += "          if (error.response.data.message){" + eol
    js += (
        "            self.props.onError(String(error.response.data.message));" + eol
    )
    js += "          } else {" + eol
    js += "            self.props.onError(String(error.response.data));" + eol
    js += "          }" + eol
    js += "        } else {" + eol
    js += "          self.props.onError(String(error.response));" + eol
    js += "        }" + eol
    js += "      } else {" + eol
    js += "        self.props.onError(String(error));" + eol
    js += "      }" + eol
    js += "    })" + eol
    js += "  } catch (err) {" + eol
    js += "    self.props.onError(String(err));" + eol
    js += "  }" + eol
    js += "}" + eol

    Component.addPropVariable(
        "onCheckSession", {"type": "func", "defaultValue": js}
    )

    js = "async (self, session_id, output)=> {" + eol

    js += (
        "      self.props.onStatusChange({'target':{ 'value' : 'Loading Results' } } );"
        + eol
    )
    if use_cache:
        js += "      var d_state = Object.assign({}, self.state);" + eol
        js += "      delete d_state['testing'];" + eol
        js += "      var str_key = JSON.stringify(d_state);" + eol
        js += (
            "      var buffer_key = new TextEncoder('utf-8').encode(str_key);" + eol
        )
        js += (
            "      var hashBuffer = await window.crypto.subtle.digest('SHA-256', buffer_key);"
            + eol
        )
        js += "      var hashArray = Array.from(new Uint8Array(hashBuffer));" + eol
        js += (
            "      var hash_key = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');"
            + eol
        )
        js += (
            "      var hash_q = await "
            + cache_store
            + ".setItem(hash_key, JSON.stringify(output), (e)=>{self.props.onError(e.toString())});"
            + eol
        )
        js += (
            "      var olist_json = await "
            + cache_store
            + ".getItem('cache_list');"
            + eol
        )
        js += "      if (!olist_json || olist_json == '')" + eol
        js += "        olist_json = '{}';" + eol
        js += "      var cacheList = JSON.parse(olist_json);" + eol
        js += "      cacheList[hash_key] = d_state;" + eol
        js += (
            "      var hash_q = await "
            + cache_store
            + ".setItem('cache_list', JSON.stringify(cacheList), (e)=>{self.props.onError(e.toString())});"
            + eol
        )
    js += "      self.props.onSuccess(self, hash_key)" + eol
    js += "}" + eol

    Component.addPropVariable("onLoadResults", {"type": "func", "defaultValue": js})

    callbacklist = []
    states_def = "{ 'target' : { 'value' : {"
    for k, state in Component.stateDefinitions.items():
        states_def += "'" + k + "': self.state." + k + " ,"
    states_def += "} } }"
    callbacklist.append(
        {"type": "propCall2", "calls": "onSimulate", "args": ["self", states_def]}
    )

    return callbacklist

def buildSchema(tp, Component, *args, **kwargs):
    store_name = "sessionStore"
    NanohubUtils.storageFactory(tp, store_name=store_name)
    toolname = kwargs.get("toolname", "")
    revision = kwargs.get("revision", "")
    url = kwargs.get("url", "https://nanohub.org/api/results/simtools")
    eol = "\n"
    js = ""
    js += "async (self) => {"
    js += "  var nanohub_token = " + store_name + ".getItem('nanohub_token');" + eol
    js += (
        "  var header_token = {'Authorization': 'Bearer ' + nanohub_token, 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*' };"
        + eol
    )
    js += (
        "  var options = { 'handleAs' : 'json' , 'headers' : header_token, 'method' : 'GET' };"
        + eol
    )
    js += (
        "  var url = '"
        + url
        + "/get/"
        + toolname
        + "/"
        + str(revision)
        + "';"
        + eol
    )
    js += "  let params = {};" + eol
    js += "  let selfr = self;" + eol
    js += "  try{" + eol
    js += "    await Axios.request(url, options)" + eol
    js += "    .then(function(response){" + eol
    js += "      var data = response.data;" + eol
    js += "      var schema = data.tool;" + eol
    js += "      var schema_json = JSON.stringify(schema);" + eol
    js += "      if (schema_json){" + eol
    js += (
        "        "
        + store_name
        + ".setItem('nanohub_tool_schema', schema_json);"
        + eol
    )
    js += "        selfr.props.onLoadSchema(selfr)"
    js += "      } else {" + eol
    js += "        selfr.props.onSchemaError(selfr)"
    js += "      }" + eol
    js += "    }).catch(function(error){" + eol
    js += "      if (error.response){" + eol
    js += "        if (error.response.data){" + eol
    js += "          if (error.response.data.message){" + eol
    js += (
        "            selfr.props.onSchemaError(String(error.response.data.message));"
        + eol
    )
    js += "          } else {" + eol
    js += (
        "            selfr.props.onSchemaError(String(error.response.data));" + eol
    )
    js += "          }" + eol
    js += "        } else {" + eol
    js += "          selfr.props.onSchemaError(String(error.response));" + eol
    js += "        }" + eol
    js += "      } else {" + eol
    js += "        selfr.props.onSchemaError(String(error));" + eol
    js += "      }" + eol
    js += "    });" + eol
    js += "  } catch (err){" + eol
    js += "    selfr.props.onSchemaError(selfr)"
    js += "  }" + eol
    js += "}" + eol

    Component.addPropVariable("buildSchema", {"type": "func", "defaultValue": js})
    Component.addPropVariable(
        "onLoadSchema", {"type": "func", "defaultValue": "(e)=>{}"}
    )
    Component.addPropVariable(
        "onSchemaError", {"type": "func", "defaultValue": "(e)=>{}"}
    )
    callbacklist = []

    callbacklist.append(
        {"type": "propCall2", "calls": "buildSchema", "args": ["self"]}
    )
    return callbacklist