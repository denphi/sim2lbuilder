import re
import json
import nanohubuidl.app as a
from nanohubuidl.teleport import NanohubUtils
 
eol = "\n"

def loadPlotly(*args, **kwargs):   
    cache_store = kwargs.get("cache_store", "CacheStore");
    js = ""
    js += "async (component, seq, layout, shapes={}) => {" + eol
    js += "  var olist_json = await " + cache_store + ".getItem('cache_list');" + eol
    js += "  if (!olist_json || olist_json == '')" + eol
    js += "    olist_json = '{}';" + eol
    js += "  let inputs = JSON.parse(olist_json);" + eol
    js += "  var cacheList = component.state.active_cache;" + eol
    js += "  let cdata = [];" + eol
    js += "  let cshapes = [];" + eol
    js += "  let plt;" + eol   
    js += "  for (const hash_ind in cacheList) {" + eol
    js += "    let hash_key = cacheList[hash_ind];" + eol
    js += "    var output_json = await " + cache_store + ".getItem(hash_key);" + eol
    js += "    if (!output_json || output_json == '')" + eol
    js += "      return;" + eol
    js += "    var jsonOutput = JSON.parse(output_json);" + eol
    js += "    var state = component.state;" + eol
    js += "    var lseq = Array();" + eol
    js += "    Object.entries(seq).forEach(([sequence,data]) => {" + eol
    js += "      let sseq = sequence.split(',')" + eol
    js += "      if (sseq.length>1){" + eol
    js += "        let merged = {};" + eol
    js += "        for (let seqi=0;seqi<sseq.length;seqi++ ){" + eol
    js += "          if (sseq[seqi] in jsonOutput){" + eol
    js += "            merged[sseq[seqi]] = jsonOutput[sseq[seqi]]" + eol
    js += "          }" + eol
    js += "        }" + eol
    js += "        jsonOutput[sequence] = merged;" + eol
    js += "      }" + eol
    js += "      if (sequence in jsonOutput){" + eol
    js += "        let curves = jsonOutput[sequence];" + eol
    js += "        let datac = JSON.parse(JSON.stringify(data));" + eol
    js += "        Object.entries(datac).forEach(([k,v]) => {" + eol
    js += "          if (v.toString().startsWith('$')){" + eol
    js += "            let label = v.toString().replace('$', '');" + eol
    js += "            if (label == 'value'){" + eol
    js += "                datac[k] = curves;" + eol
    js += "            } else if (label.startsWith('max$')){" + eol
    js += "              label = label.replace('max$', '');" + eol
    js += "              if (label in curves){" + eol
    js += "                datac[k] = [Math.max(...curves[label]),0,0,Math.max(...curves[label])];" + eol
    js += "              }" + eol
    js += "            } else if (label.startsWith('index$')){" + eol
    js += "              try {" + eol
    js += "                label = Math.trunc(Number(label.replace('index$', '')));" + eol
    js += "                label = Math.min(label, Object.keys(curves).length-1);" + eol
    js += "                if (label>0)" + eol
    js += "                  datac[k] = curves[Object.keys(curves)[label]];" + eol
    js += "              } catch {}" + eol
    js += "            } else if (label in curves){" + eol
    js += "              datac[k] = curves[label];" + eol
    js += "            }" + eol
    js += "          }" + eol
    js += "        })" + eol
    js += "        if (component.state.lastCache != hash_key) {" + eol
    js += "          if (!('line' in datac)) " + eol
    js += "            datac['line'] = {'color':'lightgrey'}; " + eol
    js += "          else " + eol
    js += "            datac['line']['color'] = 'lightgrey'; " + eol
    js += "          if (!('marker' in datac)) " + eol
    js += "            datac['marker'] = {'color':'lightgrey'}; " + eol
    js += "          else " + eol
    js += "            datac['marker']['color'] = 'lightgrey'; " + eol
    js += "          datac['colorscale']= 'Greys'; " + eol
    js += "          datac['opacity']= '0.5'; " + eol
    js += "        }" + eol
    js += "        lseq.push(datac)" + eol
    js += "      }" + eol
    js += "    });" + eol
    js += "    cdata = cdata.concat(lseq);" + eol
    js += "    lseq = Array();" + eol
    js += "    Object.entries(shapes).forEach(([sequence,data]) => {" + eol
    js += "      if (sequence in jsonOutput){" + eol
    js += "        let curves = jsonOutput[sequence];" + eol
    js += "        if (Array.isArray(curves)){" + eol
    js += "          for (let c in curves) {" + eol
    js += "            for (let d in data) {" + eol
    js += "              let data2={};" + eol
    js += "              Object.entries(data[d]).forEach(([k,v]) => {" + eol
    js += "                let value = v;" + eol
    js += "                if (typeof v === 'string'){" + eol
    js += "                  value = v.toString().replaceAll('$value', curves[c]);" + eol
    js += "                }" + eol
    js += "                data2[k] = value;" + eol
    js += "              })" + eol
    js += "              if (component.state.lastCache != hash_key) {" + eol
    js += "                data2['line'] = {'color':'lightgrey'}; " + eol
    js += "              }" + eol
    js += "              lseq.push(data2)" + eol
    js += "            }" + eol
    js += "          }" + eol
    js += "        } else{" + eol
    js += "          let curves2 = [];" + eol
    js += "          let keycurves = Object.keys(curves);" + eol 
    js += "          if (Array.isArray(curves[keycurves[0]])){" + eol
    js += "            for (let c in curves[keycurves[0]]) {" + eol
    js += "              for (let d in data) {" + eol
    js += "                let data2={};" + eol
    js += "                Object.entries(data[d]).forEach(([k,v]) => {" + eol
    js += "                  let value = v;" + eol
    js += "                  if (typeof v === 'string'){" + eol
    js += "                    value = v.toString().replaceAll('$', '$[' + (c).toString() + ']');" + eol
    js += "                  }" + eol
    js += "                  data2[k] = value;" + eol
    js += "                })" + eol
    js += "                if (component.state.lastCache != hash_key) {" + eol
    js += "                  data2['line'] = {'color':'lightgrey'}; " + eol
    js += "                }" + eol
    js += "                lseq.push(data2)" + eol
    js += "              }" + eol
    js += "            }" + eol
    js += "            const regex = /\$\[(\d)\](\w*)/g;" + eol
    js += "            let m;" + eol
    js += "            for (l in lseq){" + eol
    js += "              Object.entries(lseq[l]).forEach(([k,v]) => {" + eol
    js += "                while ((m = regex.exec(v)) !== null) {" + eol
    js += "                  if (m.index === regex.lastIndex) {" + eol
    js += "                    regex.lastIndex++;" + eol
    js += "                  }" + eol
    js += "                  lseq[l][k] = lseq[l][k].toString().replaceAll('$[' + m[1] + ']' + m[2], curves[m[2]][parseInt(m[1])])" + eol
    js += "                }" + eol
    js += "              })" + eol
    js += "            }" + eol
    js += "          }" + eol    
    js += "        }" + eol
    js += "      }" + eol
    js += "    });" + eol
    js += "    cshapes = cshapes.concat(lseq);" + eol
    js += "  }" + eol    
    js += "  layout['shapes'] = cshapes;" + eol    
    js += "  component.setState({" + eol
    js += "    'data': cdata," + eol
    js += "    'layout': layout," + eol
    js += "    'config': {" + eol
    js += "      'displayModeBar': true, " + eol
    js += "      'responsive': true, " + eol
    js += "      'displaylogo': false, " + eol
    js += "      'editable': false, " + eol
    js += "      'modeBarButtonsToAdd' : [{" + eol
    js += "        'name': 'Reset'," + eol
    js += "        'icon': Plotly.Icons.home," + eol
    js += "        'direction': 'up'," + eol
    js += "        'click': function(gd) {component.props.refreshViews(component)}" + eol
    js += "      }]," + eol
    js += "      'modeBarButtonsToRemove': ['sendDataToCloud', 'hoverClosestCartesian', 'hoverCompareCartesian', 'resetScale2d']" + eol
    js += "    }" + eol    
    js += "  });" + eol
    js += "  window.dispatchEvent(new Event('relayout'));" + eol #trying to trigger windows rescale does not work on IE
    js += "}" + eol
    return js


def loadValuePlotly(*args, **kwargs):   
    cache_store = kwargs.get("cache_store", "CacheStore");
    js = ""
    js += "async (component, seq, layout, shapes={}) => {" + eol
    js += "  var olist_json = await " + cache_store + ".getItem('cache_list');" + eol
    js += "  if (!olist_json || olist_json == '')" + eol
    js += "    olist_json = '{}';" + eol
    js += "  let inputs = JSON.parse(olist_json);" + eol
    js += "  var cacheList = component.state.active_cache;" + eol
    js += "  let cvalues = {};" + eol
    js += "  let cdata = {};" + eol
    js += "  let ccolor = {};" + eol
    js += "  let copacity = {};" + eol
    js += "  let plt;" + eol 
    js += "  for (const hash_ind in cacheList) {" + eol
    js += "    let hash_key = cacheList[hash_ind];" + eol
    js += "    var output_json = await " + cache_store + ".getItem(hash_key);" + eol
    js += "    if (!output_json || output_json == '')" + eol
    js += "      return;" + eol
    js += "    var jsonOutput = JSON.parse(output_json);" + eol
    js += "    var state = component.state;" + eol
    js += "    var lseq = Array();" + eol
    js += "    Object.entries(seq).forEach(([sequence,data]) => {" + eol
    js += "      let datac = JSON.parse(JSON.stringify(data));" + eol
    js += "      cdata[sequence] = {...cdata[sequence],...datac};" + eol
    js += "      let sseq = sequence.split(',')" + eol
    js += "      if (sseq.length>0){" + eol
    js += "        for (let seqi=0;seqi<sseq.length;seqi++ ){" + eol
    js += "          if (sseq[seqi] in jsonOutput){" + eol
    js += "            let value = jsonOutput[sseq[seqi]];" + eol
    js += "            if (!(sseq[seqi] in cvalues))" + eol
    js += "              cvalues[sseq[seqi]] = [];" + eol
    js += "            cvalues[sseq[seqi]].push(value);" + eol
    js += "            ccolor[hash_key] = '#1f77b4';" + eol
    js += "            copacity[hash_key] = 1;" + eol
    js += "            if (component.state.lastCache != hash_key){" + eol
    js += "              ccolor[hash_key] = 'lightgrey';" + eol
    js += "              copacity[hash_key] = 0.5;" + eol
    js += "            }" + eol
    js += "          }" + eol
    js += "        }" + eol
    js += "      }" + eol
    js += "    });" + eol
    js += "  }" + eol  
    js += "  try { " + eol
    js += "    Object.entries(cdata).forEach(([k1,v1]) => {" + eol
    js += "      Object.entries(v1).forEach(([k2,v2]) => {" + eol
    js += "        if (v2.toString().startsWith('$')){" + eol
    js += "          let label = v2.toString().replace('$', '');" + eol
    js += "          if (label in cvalues){" + eol
    js += "              cdata[k1][k2]= cvalues[label];" + eol    
    js += "              if (!('marker' in cdata[k1])) " + eol
    js += "                cdata[k1]['marker'] = {}; " + eol
    js += "              if (!('color' in cdata[k1]['marker'])) " + eol
    js += "                cdata[k1]['marker']['color'] = Object.values(ccolor); " + eol
    js += "              if (!('opacity' in cdata[k1]['marker'])) " + eol
    js += "                cdata[k1]['marker']['opacity'] = Object.values(copacity); " + eol
    js += "          }" + eol
    js += "        }" + eol
    js += "      });" + eol
    js += "    });" + eol
    js += "  } catch {}" + eol
    js += "  component.setState({" + eol
    js += "    'data': Object.values(cdata)," + eol
    js += "    'layout': layout," + eol
    js += "    'config': {" + eol
    js += "      'displayModeBar': true, " + eol
    js += "      'responsive': true, " + eol
    js += "      'displaylogo': false, " + eol
    js += "      'editable': false, " + eol
    js += "    }" + eol    
    js += "  });" + eol
    js += "  window.dispatchEvent(new Event('relayout'));" + eol #trying to trigger windows rescale does not work on IE
    js += "}" + eol
    return js


def loadHTML(*args, **kwargs):
    cache_store = kwargs.get("cache_store", "CacheStore");

    js = ""
    js += "async (component, seq) => {" + eol
    js += "  var olist_json = await " + cache_store + ".getItem('cache_list');" + eol
    js += "  if (!olist_json || olist_json == '')" + eol
    js += "    olist_json = '{}';" + eol
    js += "  let inputs = JSON.parse(olist_json);" + eol
    js += "  var cacheList = component.state.active_cache;" + eol
    js += "  let cdata = document.createElement('div');" + eol
    js += "  let plt;" + eol 
    js += "  function appendDom(jsonData, data) {" + eol 
    js += "    let divParent;" + eol 
    js += "    if ('type' in jsonData){" + eol 
    js += "      divParent  = document.createElement(jsonData.type);" + eol 
    js += "      Object.entries(jsonData).forEach(([attr,value]) => {" + eol
    js += "        try {" + eol 
    js += "          if (attr == 'type') {" + eol
    js += "          } else if (attr == 'textContent') {" + eol 
    js += "              if (value == '$value')" + eol 
    js += "                divParent.textContent = data;" + eol 
    js += "              else" + eol 
    js += "                divParent.textContent = value;" + eol 
    js += "          } else if (attr == 'children') {" + eol 
    js += "            for (var i = 0; i <value.length; i++) {" + eol 
    js += "              divParent.append(appendDom(value[i], data));" + eol 
    js += "            }" + eol 
    js += "          } else {" + eol 
    js += "            if (value == '$value')" + eol 
    js += "              divParent.setAttribute(attr,data);" + eol 
    js += "            else" + eol 
    js += "              divParent.setAttribute(attr,value);" + eol 
    js += "          } " + eol
    js += "        } catch { } " + eol
    js += "      });" + eol 
    js += "    } else{ " + eol 
    js += "      divParent = document.createElement('div');" + eol 
    js += "    }" + eol 
    js += "    return divParent" + eol 
    js += "  }" + eol 
    js += "  for (const hash_ind in cacheList) {" + eol
    js += "    let hash_key = cacheList[hash_ind];" + eol
    js += "    var output_json = await " + cache_store + ".getItem(hash_key);" + eol
    js += "    if (!output_json || output_json == '')" + eol
    js += "      return;" + eol
    js += "    var jsonOutput = JSON.parse(output_json);" + eol
    js += "    var state = component.state;" + eol
    js += "    var lseq = Array();" + eol
    js += "    Object.entries(seq).forEach(([sequence,data]) => {" + eol
    js += "      let datac = JSON.parse(JSON.stringify(data));" + eol
    js += "      if (sequence in jsonOutput){" + eol
    js += "        let dom = appendDom(datac, jsonOutput[sequence]);" + eol
    js += "        if (component.state.lastCache != hash_key)" + eol
    js += "          dom.setAttribute('style', 'border: 10px solid lightgrey');" + eol
    js += "        else" + eol
    js += "          dom.setAttribute('style', 'border: 10px solid #1f77b4');" + eol
    js += "        cdata.append(dom)" + eol
    js += "      }" + eol
    js += "    });" + eol
    js += "  }" + eol  
    js += "  try { " + eol
    js += "  } catch {}" + eol
    js += "  component.setState({" + eol
    js += "    'src_detail': { '__html': cdata.innerHTML }," + eol
    js += "    'data': []," + eol
    js += "    'layout': {}," + eol
    js += "    'config': {" + eol
    js += "      'displayModeBar': true, " + eol
    js += "      'responsive': true, " + eol
    js += "      'displaylogo': false, " + eol
    js += "      'editable': false, " + eol
    js += "    }" + eol    
    js += "  });" + eol
    js += "  window.dispatchEvent(new Event('relayout'));" + eol #trying to trigger windows rescale does not work on IE
    js += "}" + eol
    return js


def loadTablePlotly(*args, **kwargs):   
    cache_store = kwargs.get("cache_store", "CacheStore");
    js = ""
    js += "async (component, seq, layout, shapes={}) => {" + eol
    js += "  var olist_json = await " + cache_store + ".getItem('cache_list');" + eol
    js += "  if (!olist_json || olist_json == '')" + eol
    js += "    olist_json = '{}';" + eol
    js += "  let inputs = JSON.parse(olist_json);" + eol
    js += "  var cacheList = component.state.active_cache;" + eol
    js += "  let ccells = {};" + eol
    js += "  let cheader = {};" + eol
    js += "  let cdata = {};" + eol
    js += "  let ccolor = {};" + eol
    js += "  let plt;" + eol 
    js += "  for (const hash_ind in cacheList) {" + eol
    js += "    let hash_key = cacheList[hash_ind];" + eol
    js += "    var output_json = await " + cache_store + ".getItem(hash_key);" + eol
    js += "    if (!output_json || output_json == '')" + eol
    js += "      return;" + eol
    js += "    var jsonOutput = JSON.parse(output_json);" + eol
    js += "    var state = component.state;" + eol
    js += "    var lseq = Array();" + eol
    js += "    Object.entries(seq).forEach(([sequence,data]) => {" + eol
    js += "      let datac = JSON.parse(JSON.stringify(data));" + eol
    js += "      cdata = {...cdata,...datac};" + eol
    js += "      if (sequence in jsonOutput){" + eol
    js += "        let cell = '';" + eol
    js += "        try {" + eol
    js += "          if (datac.cells.values == '$value'){" + eol
    js += "            cell = jsonOutput[sequence];" + eol
    js += "          } else {" + eol
    js += "            cell = datac.cells.values;" + eol
    js += "          }" + eol
    js += "        } catch {" + eol
    js += "          cell = '';" + eol
    js += "        } " + eol
    js += "        if (!(sequence in ccells))" + eol
    js += "          ccells[sequence] = [];" + eol
    js += "        ccells[sequence].push(cell);" + eol
    js += "        let header = '';" + eol
    js += "        try {" + eol
    js += "          if (datac.header.values == '$value'){" + eol
    js += "            header = sequence;" + eol
    js += "          } else {" + eol
    js += "            header = datac.header.values;" + eol
    js += "          }" + eol
    js += "        } catch {" + eol
    js += "          header = '';" + eol
    js += "        } " + eol
    js += "        if (!(sequence in cheader))" + eol
    js += "          cheader[sequence] = [header];" + eol
    js += "        if (component.state.lastCache != hash_key) {" + eol
    js += "          ccolor[hash_key] = 'lightgrey';" + eol
    js += "        } else {" + eol
    js += "          ccolor[hash_key] = '#1f77b4';" + eol
    js += "        }" + eol
    js += "      }" + eol
    js += "    });" + eol
    js += "  }" + eol  
    js += "  try { " + eol
    js += "    if (!('header' in cdata))" + eol
    js += "      cdata.header = {};" + eol
    js += "    if (!('values' in cdata.header))" + eol
    js += "      cdata.values = [];" + eol
    js += "    if (cdata.header.values == '$value')" + eol
    js += "      cdata.header.values = Object.values(cheader);" + eol
    js += "    if (!('cells' in cdata))" + eol
    js += "      cdata.cells = {};" + eol
    js += "    if (!('values' in cdata.cells))" + eol
    js += "      cdata.cells.values = [];" + eol
    js += "    if (cdata.cells.values == '$value')" + eol
    js += "      cdata.cells.values = Object.values(ccells);" + eol
    js += "      if (!('fill' in cdata.cells))" + eol
    js += "        cdata.cells.fill = {};" + eol
    js += "      cdata.cells.fill.color = [Object.values(ccolor)];" + eol
    js += "    cdata.type = 'table';" + eol
    js += "  } catch {}" + eol
    js += "  component.setState({" + eol
    js += "    'data': [cdata]," + eol
    js += "    'layout': layout," + eol
    js += "    'config': {" + eol
    js += "      'displayModeBar': true, " + eol
    js += "      'responsive': true, " + eol
    js += "      'displaylogo': false, " + eol
    js += "      'editable': false, " + eol
    js += "    }" + eol    
    js += "  });" + eol
    js += "  window.dispatchEvent(new Event('relayout'));" + eol #trying to trigger windows rescale does not work on IE
    js += "}" + eol
    return js

def loadSequencePlotly(*args, **kwargs):   
    cache_store = kwargs.get("cache_store", "CacheStore");
    js = ""
    js += "async (component, seq, layout, normalize=false, starting=0) => {" + eol
    js += "  var olist_json = await " + cache_store + ".getItem('cache_list');" + eol
    js += "  if (!olist_json || olist_json == '')" + eol
    js += "    olist_json = '{}';" + eol
    js += "  let inputs = JSON.parse(olist_json);" + eol
    js += "  var cacheList = component.state.active_cache;" + eol
    js += "  let cframes = {};" + eol
    js += "  let cdata = [];" + eol
    js += "  let plt;" + eol   
    js += "  var min_tr_x = undefined;" + eol
    js += "  var min_tr_y = undefined;" + eol
    js += "  var max_tr_x = undefined;" + eol
    js += "  var max_tr_y = undefined;" + eol
    js += "  for (const hash_ind in cacheList) {" + eol
    js += "    let hash_key = cacheList[hash_ind];" + eol
    js += "    var output_json = await " + cache_store + ".getItem(hash_key);" + eol
    js += "    if (!output_json || output_json == '')" + eol
    js += "      return;" + eol
    js += "    var jsonOutput = JSON.parse(output_json);" + eol
    js += "    var state = component.state;" + eol
    js += "    var lseq = Array();" + eol
    js += "    Object.entries(seq).forEach(([sequence,data]) => {" + eol
    js += "      let sseq = sequence.split(',')" + eol
    js += "      if (sseq.length>1){" + eol
    js += "        let merged = {};" + eol
    js += "        for (let seqi=0;seqi<sseq.length;seqi++ ){" + eol
    js += "          if (sseq[seqi] in jsonOutput){" + eol
    js += "            merged[sseq[seqi]] = jsonOutput[sseq[seqi]]" + eol
    js += "          }" + eol
    js += "        }" + eol
    js += "        jsonOutput[sequence] = merged;" + eol
    js += "      }" + eol
    js += "      if (sequence in jsonOutput){" + eol
    js += "        let mcurves = jsonOutput[sequence];" + eol
    js += "        let pos = 0;" + eol
    js += "        if (data.unique){ " + eol
    js += "          mcurves = {}" + eol
    js += "          Object.entries(cframes).forEach(([k,c]) => {" + eol
    js += "            mcurves[k] = jsonOutput[sequence];" + eol
    js += "          });" + eol 
    js += "        }" + eol 
    js += "        Object.entries(mcurves).forEach(([key,c]) => {" + eol
    js += "          let curves = mcurves[key]; " + eol
    js += "          if (!(key in cframes))" + eol
    js += "            cframes[key] = [];" + eol
    js += "          let datac = JSON.parse(JSON.stringify(data));" + eol
    js += "          Object.entries(datac).forEach(([k,v]) => {" + eol
    js += "            if (v.toString().startsWith('$')){" + eol
    js += "              let label = v.toString().replace('$', '');" + eol
    js += "              if (label == 'value'){" + eol
    js += "                  datac[k] = curves;" + eol
    js += "              } if (label.startsWith('max$')){" + eol
    js += "                label = label.replace('max$', '');" + eol
    js += "                if (label in curves){" + eol
    js += "                  datac[k] = [Math.max(...curves[label]),0,0,Math.max(...curves[label])];" + eol
    js += "                }" + eol
    js += "              } else if (label.startsWith('index$')){" + eol
    js += "                try {" + eol
    js += "                  label = Math.trunc(Number(label.replace('index$', '')));" + eol
    js += "                  label = Math.min(label, Object.keys(curves).length-1);" + eol
    js += "                  if (label>0)" + eol
    js += "                    datac[k] = curves[Object.keys(curves)[label]];" + eol
    js += "                } catch {}" + eol
    js += "              } else if (label in curves){" + eol
    js += "                datac[k] = curves[label];" + eol
    js += "              }" + eol
    js += "            }" + eol
    js += "          })" + eol
    js += "          if (component.state.lastCache != hash_key) {" + eol
    js += "            if (!('line' in datac)) " + eol
    js += "              datac['line'] = {'color':'lightgrey'}; " + eol
    js += "            else " + eol
    js += "              datac['line']['color'] = 'lightgrey'; " + eol
    js += "            if (!('marker' in datac)) " + eol
    js += "              datac['marker'] = {'color':'lightgrey'}; " + eol
    js += "            else " + eol
    js += "              datac['marker']['color'] = 'lightgrey'; " + eol
    js += "            datac['colorscale']= 'Greys'; " + eol
    js += "            datac['opacity']= '0.5'; " + eol
    js += "          }" + eol
    js += "          cframes[key].push(datac);" + eol
    js += "          var minx, maxx;" + eol
    js += "          try {" + eol
    js += "            if (min_tr_x ==undefined)" + eol
    js += "              min_tr_x = Math.min(...datac['x']);" + eol
    js += "            min_tr_x = Math.min(min_tr_x,...datac['x']);" + eol
    js += "            if (max_tr_x ==undefined)" + eol
    js += "              max_tr_x = Math.max(...datac['x']);" + eol
    js += "            max_tr_x = Math.max(max_tr_x,...datac['x']);" + eol
    js += "          } catch(error){}" + eol
    js += "          try {" + eol
    js += "            if (min_tr_y ==undefined)" + eol
    js += "              min_tr_y = Math.min(...datac['y']);" + eol
    js += "            min_tr_y = Math.min(min_tr_y,...datac['y']);" + eol
    js += "            if (max_tr_y ==undefined)" + eol
    js += "              max_tr_y = Math.max(...datac['y']);" + eol
    js += "            max_tr_y = Math.max(max_tr_y,...datac['y']);" + eol
    js += "          } catch(error) {}" + eol    
    js += "        })" + eol
    js += "      }" + eol
    js += "    });" + eol
    js += "  }" + eol  
    js += "  if (!layout['xaxis'])" + eol  
    js += "    layout['xaxis'] = {};" + eol  
    js += "  if (!layout['yaxis'])" + eol  
    js += "    layout['yaxis'] = {};" + eol  
    js += "  if (normalize && !isNaN(min_tr_x) && !isNaN(max_tr_x)){" + eol
    js += "    layout['xaxis']['autorange']=false;" + eol
    js += "    layout['xaxis']['range']=[min_tr_x, max_tr_x];" + eol
    js += "  } if (normalize && !isNaN(min_tr_y) && !isNaN(max_tr_y)) {" + eol
    js += "    layout['yaxis']['autorange']=false;" + eol
    js += "    layout['yaxis']['range']=[min_tr_y, max_tr_y];" + eol
    js += "  } " + eol
    js += "  if (layout['xaxis'] && layout['xaxis']['type'] && layout['xaxis']['type'] == 'log'){" + eol
    js += "    if (layout['xaxis']['range'][0] == 0){" + eol
    js += "      layout['xaxis']['range'][0] = 1e-20;" + eol
    js += "    }" + eol
    js += "    layout['xaxis']['range'][0] = Math.log10(layout['xaxis']['range'][0]);" + eol
    js += "    layout['xaxis']['range'][1] = Math.log10(layout['xaxis']['range'][1]);" + eol
    js += "  }" + eol
    js += "  if (layout['yaxis'] && layout['yaxis']['type'] && layout['yaxis']['type'] == 'log'){" + eol
    js += "    if (layout['yaxis']['range'][0] == 0){" + eol
    js += "      layout['yaxis']['range'][0] = 1e-20;" + eol
    js += "    }" + eol
    js += "    layout['yaxis']['range'][0] = Math.log10(layout['yaxis']['range'][0]);" + eol
    js += "    layout['yaxis']['range'][1] = Math.log10(layout['yaxis']['range'][1]);" + eol
    js += "  }" + eol
    js += "  layout['sliders'] = [{" + eol
    js += "    'pad': {t: 30}," + eol
    js += "    'x': 0.05," + eol
    js += "    'active': starting," + eol
    js += "    'len': 0.95," + eol
    js += "    'currentvalue': {" + eol
    js += "      'xanchor': 'right'," + eol
    js += "      'prefix': ''," + eol
    js += "      'font': {" + eol
    js += "        'color': '#888'," + eol
    js += "        'size': 20" + eol
    js += "      }" + eol
    js += "    }," + eol
    js += "    'transition': {'duration': 100}," + eol
    js += "    'steps': []," + eol
    js += "  }];" + eol   
    js += "  cframes = Object.keys(cframes).map((key, index) => ({" + eol
    js += "    data: cframes[key]," + eol
    js += "    name: key" + eol
    js += "  }));" + eol
    js += "  for(var f=0;f<cframes.length;f++){" + eol
    js += "    layout['sliders'][0]['steps'].push({" + eol
    js += "      label : cframes[f]['name']," + eol
    js += "      method : 'animate'," + eol
    js += "      args : [[cframes[f]['name']], {" + eol
    js += "        'mode': 'immediate'," + eol
    js += "        'frame' : {'duration': 0, 'redraw': true}," + eol
    js += "      }]" + eol
    js += "    });" + eol
    js += "  }" + eol
    js += "  if (starting<cframes.length)" + eol
    js += "    cdata = JSON.parse(JSON.stringify(cframes[starting].data));" + eol
    js += "  component.setState({" + eol
    js += "    'data': cdata," + eol
    js += "    'frames': cframes," + eol
    js += "    'layout': layout," + eol
    js += "    'config': {" + eol
    js += "      'displayModeBar': true, " + eol
    js += "      'responsive': true, " + eol
    js += "      'displaylogo': false, " + eol
    js += "      'editable': false, " + eol
    js += "      'modeBarButtonsToAdd' : [{" + eol
    js += "        'name': 'Reset'," + eol
    js += "        'icon': Plotly.Icons.home," + eol
    js += "        'direction': 'up'," + eol
    js += "        'click': function(gd) {component.props.refreshViews(component)}" + eol
    js += "      }]," + eol
    js += "      'modeBarButtonsToRemove': ['sendDataToCloud', 'hoverClosestCartesian', 'hoverCompareCartesian', 'resetScale2d']" + eol
    js += "    }" + eol    
    js += "  });" + eol
    js += "  window.dispatchEvent(new Event('relayout'));" + eol #trying to trigger windows rescale does not work on IE
    js += "}" + eol
    return js


def loadMultiPlotly(*args, **kwargs):   
    cache_store = kwargs.get("cache_store", "CacheStore");
    js = ""
    js += "async (component, seq, layout, shapes={}) => {" + eol
    js += "  var olist_json = await " + cache_store + ".getItem('cache_list');" + eol
    js += "  if (!olist_json || olist_json == '')" + eol
    js += "    olist_json = '{}';" + eol
    js += "  let inputs = JSON.parse(olist_json);" + eol
    js += "  var cacheList = component.state.active_cache;" + eol
    js += "  let cdata = [];" + eol
    js += "  let cshapes = [];" + eol
    js += "  let plt;" + eol   
    js += "  for (const hash_ind in cacheList) {" + eol
    js += "    let hash_key = cacheList[hash_ind];" + eol
    js += "    var output_json = await " + cache_store + ".getItem(hash_key);" + eol
    js += "    if (!output_json || output_json == '')" + eol
    js += "      return;" + eol
    js += "    var jsonOutput = JSON.parse(output_json);" + eol
    js += "    var state = component.state;" + eol
    js += "    var lseq = Array();" + eol
    js += "    Object.entries(seq).forEach(([sequence,data]) => {" + eol
    js += "      let sseq = sequence.split(',')" + eol
    js += "      if (sseq.length>1){" + eol
    js += "        let merged = {};" + eol
    js += "        for (let seqi=0;seqi<sseq.length;seqi++ ){" + eol
    js += "          if (sseq[seqi] in jsonOutput){" + eol
    js += "            merged[sseq[seqi]] = jsonOutput[sseq[seqi]]" + eol
    js += "          }" + eol
    js += "        }" + eol
    js += "        jsonOutput[sequence] = merged;" + eol
    js += "      }" + eol
    js += "      if (sequence in jsonOutput){" + eol
    js += "        let curvesm = jsonOutput[sequence];" + eol
    js += "        Object.entries(curvesm).forEach(([k2,curves]) => {" + eol
    js += "          let datac = JSON.parse(JSON.stringify(data));" + eol
    js += "          Object.entries(datac).forEach(([k,v]) => {" + eol
    js += "            if (v.toString().startsWith('$')){" + eol
    js += "              let label = v.toString().replace('$', '');" + eol
    js += "              if (label in curves){" + eol
    js += "                datac[k] = curves[label];" + eol
    js += "              }" + eol
    js += "            }" + eol
    js += "          })" + eol
    js += "          if (name in datac)" + eol
    js += "            datac['name'] = datac['name'] + ' ' +k2" + eol
    js += "          else " + eol
    js += "            datac['name'] = k2" + eol
    js += "          if (component.state.lastCache != hash_key) {" + eol
    js += "            if (!('line' in datac)) " + eol
    js += "              datac['line'] = {'color':'lightgrey'}; " + eol
    js += "            else " + eol
    js += "              datac['line']['color'] = 'lightgrey'; " + eol
    js += "            if (!('marker' in datac)) " + eol
    js += "              datac['marker'] = {'color':'lightgrey'}; " + eol
    js += "            else " + eol
    js += "              datac['marker']['color'] = 'lightgrey'; " + eol
    js += "          datac['colorscale']= 'Greys'; " + eol
    js += "          datac['opacity']= '0.5'; " + eol
    js += "          }" + eol
    js += "          lseq.push(datac)" + eol
    js += "        })" + eol
    js += "      }" + eol
    js += "    });" + eol
    js += "    cdata = cdata.concat(lseq);" + eol
    js += "    lseq = Array();" + eol
    js += "    Object.entries(shapes).forEach(([sequence,data]) => {" + eol
    js += "      if (sequence in jsonOutput){" + eol
    js += "        let curves = jsonOutput[sequence];" + eol
    js += "        if (Array.isArray(curves)){" + eol
    js += "          for (let c in curves) {" + eol
    js += "            for (let d in data) {" + eol
    js += "              let data2={};" + eol
    js += "              Object.entries(data[d]).forEach(([k,v]) => {" + eol
    js += "                let value = v;" + eol
    js += "                if (typeof v === 'string'){" + eol
    js += "                  value = v.toString().replaceAll('$value', curves[c]);" + eol
    js += "                }" + eol
    js += "                data2[k] = value;" + eol
    js += "              })" + eol
    js += "              if (component.state.lastCache != hash_key) {" + eol
    js += "                data2['line'] = {'color':'lightgrey'}; " + eol
    js += "              }" + eol
    js += "              lseq.push(data2)" + eol
    js += "            }" + eol
    js += "          }" + eol
    js += "        } else{" + eol
    js += "          let curves2 = [];" + eol
    js += "          let keycurves = Object.keys(curves);" + eol 
    js += "          if (Array.isArray(curves[keycurves[0]])){" + eol
    js += "            for (let c in curves[keycurves[0]]) {" + eol
    js += "              for (let d in data) {" + eol
    js += "                let data2={};" + eol
    js += "                Object.entries(data[d]).forEach(([k,v]) => {" + eol
    js += "                  let value = v;" + eol
    js += "                  if (typeof v === 'string'){" + eol
    js += "                    value = v.toString().replaceAll('$', '$[' + (c).toString() + ']');" + eol
    js += "                  }" + eol
    js += "                  data2[k] = value;" + eol
    js += "                })" + eol
    js += "                if (component.state.lastCache != hash_key) {" + eol
    js += "                  data2['line'] = {'color':'lightgrey'}; " + eol
    js += "                }" + eol
    js += "                lseq.push(data2)" + eol
    js += "              }" + eol
    js += "            }" + eol
    js += "            const regex = /\$\[(\d)\](\w*)/g;" + eol
    js += "            let m;" + eol
    js += "            for (l in lseq){" + eol
    js += "              Object.entries(lseq[l]).forEach(([k,v]) => {" + eol
    js += "                while ((m = regex.exec(v)) !== null) {" + eol
    js += "                  if (m.index === regex.lastIndex) {" + eol
    js += "                    regex.lastIndex++;" + eol
    js += "                  }" + eol
    js += "                  lseq[l][k] = lseq[l][k].toString().replaceAll('$[' + m[1] + ']' + m[2], curves[m[2]][parseInt(m[1])])" + eol
    js += "                }" + eol
    js += "              })" + eol
    js += "            }" + eol
    js += "          }" + eol    
    js += "        }" + eol
    js += "      }" + eol
    js += "    });" + eol
    js += "    cshapes = cshapes.concat(lseq);" + eol
    js += "  }" + eol    
    js += "  layout['shapes'] = cshapes;" + eol    
    js += "  component.setState({" + eol
    js += "    'data': cdata," + eol
    js += "    'layout': layout," + eol
    js += "    'config': {" + eol
    js += "      'displayModeBar': true, " + eol
    js += "      'responsive': true, " + eol
    js += "      'displaylogo': false, " + eol
    js += "      'editable': false, " + eol
    js += "      'modeBarButtonsToAdd' : [{" + eol
    js += "        'name': 'Reset'," + eol
    js += "        'icon': Plotly.Icons.home," + eol
    js += "        'direction': 'up'," + eol
    js += "        'click': function(gd) {component.props.refreshViews(component)}" + eol
    js += "      }]," + eol
    js += "      'modeBarButtonsToRemove': ['sendDataToCloud', 'hoverClosestCartesian', 'hoverCompareCartesian', 'resetScale2d']" + eol
    js += "    }" + eol    
    js += "  });" + eol
    js += "  window.dispatchEvent(new Event('relayout'));" + eol #trying to trigger windows rescale does not work on IE
    js += "}" + eol
    return js



def squidDetail(*args, **kwargs):   
    cache_store = kwargs.get("cache_store", "CacheStore");
    tn = kwargs.get("tn", "");
    js = "async (component)=>{" + eol    
    js += "  let selfr = component;" + eol
    js += "  if (!component.state.lastCache)" + eol
    js += "    return;" + eol
    js += "  var output_json = await " + cache_store + ".getItem(component.state.lastCache);" + eol
    js += "  if (!output_json || output_json == '')" + eol
    js += "    return;" + eol
    js += "  var jsonOutput = JSON.parse(output_json);" + eol  
    js += "  if ('_id_' in jsonOutput){" + eol
    js += "    const regex = /\/(\d*)\//i;" + eol
    js += "    window.open('https://nanohub.org/results/results/" + tn + "?squid=' + jsonOutput['_id_'].replace(regex, '_r$1_'), '"+tn+"_details', 'toolbar=0,location=0,menubar=0');" + eol
    js += "  }" + eol
    js += "}" + eol
    return js

def refreshViews(tp, tc, *args, **kwargs):  
    cache_store = kwargs.get("cache_store", "CacheStore");
    enable_compare = kwargs.get("enable_compare", True);
    views = kwargs.get("views", {});
    cache_storage = kwargs.get("cache_storage", "cacheFactory('"+cache_store+"', 'INDEXEDDB')")
    NanohubUtils.storageFactory(tp, store_name=cache_store, storage_name=cache_storage)          
    regc = tp.project_name    
    regc = "_" + re.sub("[^a-zA-Z0-9]+", "", regc) + "_"
    js = "async (component)=>{" + eol    
    js += "  let selfr = component;" + eol
    js += "  var listState = [];" + eol
    js += "  var activeCache = [];" + eol
    js += "  let enable_history = false;" + eol
    js += "  if (" + cache_store + "){" + eol
    if enable_compare:
        js += "    var olen = await " + cache_store + ".length();" + eol
        js += "    for (let ii=0; ii<olen; ii++) {" + eol
        js += "      var key = await " + cache_store + ".key(ii);" + eol
        js += "      //const regex = new RegExp('" + regc + "([a-z0-9]{64})', 'im');" + eol
        js += "      //let m;" + eol
        js += "      if (key.startsWith('" + regc + "')) {" + eol
        js += "        let m = [0,key.replace('" + regc + "','')];" + eol
        js += "        if (m[1].length == 64) {" + eol
        js += "          if (component.state.lastCache == m[1]){ " + eol
        js += "            activeCache.push(m[1]);" + eol
        js += "          } else if (component.state.compare){ " + eol
        js += "            activeCache.push(m[1]);" + eol
        js += "            enable_history = true;" + eol
        js += "          } else {" + eol
        js += "            enable_history = true;" + eol
        js += "          }" + eol
        js += "        }" + eol
        js += "      }" + eol
        js += "    }" + eol
    else :
        js += "    if (component.state.lastCache != ''){" + eol
        js += "      activeCache.push(component.state.lastCache);" + eol
        js += "    }" + eol

    js += "    selfr.setState({'enable_history': enable_history, 'active_cache':activeCache});" + eol
    js += "    let vis = selfr.state['visualization']; " + eol
    js += "    selfr.setState({'open_plot':selfr.state.visualization.id});" + eol
    for k,v in views.items():
        props = ["selfr"]
        state = {}
        name = str(k)
        if "params" in v:
            props = props + ["vis['" + str(v2) + "']" for v2 in v["params"]]
        if "state" in v:
            state = json.dumps(v["state"])
        js += "    if (vis['function'] == '"+name+"'){" + eol
        js += "        selfr.setState("+state+", () => {" + eol
        js += "          selfr.props."+name+"(" + ",".join(props) + ");" + eol
        js += "        });" + eol
        js += "    }" + eol
    js += "  }" + eol
    js += "}" + eol
    tc.addPropVariable("refreshViews", {"type":"func", 'defaultValue' :js})   

    return [
      {
        "type": "propCall2",
        "calls": "refreshViews",
        "args": ['self', '']
      }
    ] 