import re
import nanohubuidl.teleport as t
import nanohubuidl.app as a
import nanohubuidl.material as m
from nanohubuidl.simtool import SimtoolBuilder
from .components import *
import json

def loadPlotly(tp, tc, *args, **kwargs):   
    eol = "\n";
    cache_store = kwargs.get("cache_store", "CacheStore");
    cache_storage = kwargs.get("cache_storage", "cacheFactory('"+cache_store+"', 'INDEXEDDB')")
    t.NanohubUtils.storageFactory(tp, store_name=cache_store, storage_name=cache_storage)        

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
    js += "          if (sseq[i] in jsonOutput){" + eol
    js += "            merged[sseq[i]] = jsonOutput[sseq[i]]" + eol
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
    tc.addPropVariable("loadPlotly", {"type":"func", "defaultValue": js})    

    return {
      "type": "propCall2",
      "calls": "loadPlotly",
      "args": ['self', '[]']
    }


def loadSequencePlotly(tp, tc, *args, **kwargs):   
    eol = "\n";
    cache_store = kwargs.get("cache_store", "CacheStore");
    cache_storage = kwargs.get("cache_storage", "cacheFactory('"+cache_store+"', 'INDEXEDDB')")
    t.NanohubUtils.storageFactory(tp, store_name=cache_store, storage_name=cache_storage)        

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
    js += "          if (sseq[i] in jsonOutput){" + eol
    js += "            merged[sseq[i]] = jsonOutput[sseq[i]]" + eol
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
    tc.addPropVariable("loadSequencePlotly", {"type":"func", "defaultValue": js})    

    return {
      "type": "propCall2",
      "calls": "loadSequencePlotly",
      "args": ['self', '[]']
    }

def loadMultiPlotly(tp, tc, *args, **kwargs):   
    eol = "\n";
    cache_store = kwargs.get("cache_store", "CacheStore");
    cache_storage = kwargs.get("cache_storage", "cacheFactory('"+cache_store+"', 'INDEXEDDB')")
    t.NanohubUtils.storageFactory(tp, store_name=cache_store, storage_name=cache_storage)        

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
    js += "          if (sseq[i] in jsonOutput){" + eol
    js += "            merged[sseq[i]] = jsonOutput[sseq[i]]" + eol
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
    tc.addPropVariable("loadMultiPlotly", {"type":"func", "defaultValue": js})    

    return {
      "type": "propCall2",
      "calls": "loadMultiPlotly",
      "args": ['self', '[]']
    }


def squidDetail(tp, tc, tn, *args, **kwargs):   
    eol = "\n";
    cache_store = kwargs.get("cache_store", "CacheStore");
    cache_storage = kwargs.get("cache_storage", "cacheFactory('"+cache_store+"', 'INDEXEDDB')")
    t.NanohubUtils.storageFactory(tp, store_name=cache_store, storage_name=cache_storage)          

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
    js += "    window.open('https://nanohub.org/results/results/" + tn + "?squid=' + jsonOutput['_id_'].replace(regex, '_r$1_'), '_blank', 'toolbar=0,location=0,menubar=0');" + eol
    #js += "    component.setState({'src_detail':'https://nanohub.org/results/results/st4pcpbt?squid=' + jsonOutput['_id_'].replaceAll('/','_')});" + eol
    js += "  }" + eol
    js += "}" + eol
    tc.addPropVariable("squidDetail", {"type":"func", 'defaultValue' :js})   

    return [
      {
        "type": "propCall2",
        "calls": "squidDetail",
        "args": ['self', '']
      }
    ] 

def refreshViews(tp, tc, *args, **kwargs):  

    eol = "\n";
    cache_store = kwargs.get("cache_store", "CacheStore");
    cache_storage = kwargs.get("cache_storage", "cacheFactory('"+cache_store+"', 'INDEXEDDB')")
    t.NanohubUtils.storageFactory(tp, store_name=cache_store, storage_name=cache_storage)          
    regc = tp.project_name    
    regc = "_" + re.sub("[^a-zA-Z0-9]+", "", regc) + "_"
    js = "async (component)=>{" + eol    
    js += "  let selfr = component;" + eol
    js += "  var listState = [];" + eol
    js += "  var activeCache = [];" + eol
    js += "  if (" + cache_store + "){" + eol
    js += "    var olen = await " + cache_store + ".length();" + eol
    js += "    for (let ii=0; ii<olen; ii++) {" + eol
    js += "      var key = await " + cache_store + ".key(ii);" + eol
    js += "      const regex = new RegExp(' " + regc + "([a-z0-9]{64})', 'im');" + eol
    js += "      let m;" + eol
    js += "      if ((m = regex.exec(key)) !== null) {" + eol
    js += "          if (component.state.lastCache == m[1]){ " + eol
    js += "              activeCache.push(m[1]);" + eol
    js += "          } else if (component.state.compare){ " + eol
    js += "              activeCache.push(m[1]);" + eol
    js += "          }" + eol
    js += "          listState.push({" + eol
    js += "            'id':m[1]," + eol
    js += "            'icon':'show_chart'," + eol
    js += "            'value':m[1]," + eol
    js += "          });" + eol
    js += "          " + eol
    js += "      };" + eol
    js += "    }" + eol
    js += "    selfr.setState({'cached_results':listState});" + eol
    js += "    selfr.setState({'active_cache':activeCache});" + eol
    js += "    let vis = selfr.state['visualization']; " + eol
    js += "    selfr.setState({'open_plot':selfr.state.visualization.id});" + eol
    js += "    if (vis['function'] == 'loadPlotly'){" + eol
    js += "        selfr.props.loadPlotly(selfr, vis['dataset'], vis['layout'], vis['shapes']);" + eol
    js += "        selfr.setState({'open_params':false});" + eol
    js += "        selfr.setState({'open_details':false});" + eol
    js += "    } else if (vis['function'] == 'loadSequencePlotly'){" + eol
    js += "        selfr.props.loadSequencePlotly(selfr, vis['dataset'], vis['layout'], vis['normalize'], vis['start_trace']);" + eol
    js += "        selfr.setState({'open_params':false});" + eol
    js += "        selfr.setState({'open_details':false});" + eol
    js += "    } else if (vis['function'] == 'loadMultiPlotly'){" + eol
    js += "        selfr.props.loadMultiPlotly(selfr, vis['dataset'], vis['layout'], vis['shapes']);" + eol
    js += "        selfr.setState({'open_params':false});" + eol
    js += "        selfr.setState({'open_details':false});" + eol
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


def deleteHistory(tp, tc, *args, **kwargs):   
    eol = "\n";
    cache_store = kwargs.get("cache_store", "CacheStore");
    cache_storage = kwargs.get("cache_storage", "cacheFactory('"+cache_store+"', 'INDEXEDDB')")
    t.NanohubUtils.storageFactory(tp, store_name=cache_store, storage_name=cache_storage)          

    regc = tp.project_name    
    regc = "_" + re.sub("[^a-zA-Z0-9]+", "", regc) + "_"

    js = "async (component)=>{" + eol    
    js += "  let selfr = component;" + eol
    js += "  var listState = [];" + eol
    js += "  var activeCache = [];" + eol
    js += "  var olen = await " + cache_store + ".length();" + eol
    js += "  for (let ii=0; ii<olen; ii++) {" + eol
    js += "    var key = await " + cache_store + ".key(ii);" + eol
    js += "    const regex = new RegExp(' " + regc + "([a-z0-9]{64})', 'im');" + eol
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
    cache_storage = kwargs.get("cache_storage", "cacheFactory('"+cache_store+"', 'INDEXEDDB')")
    t.NanohubUtils.storageFactory(tp, store_name=cache_store, storage_name=cache_storage)          

    js = "async (component)=>{" + eol    
    js += "  let selfr = component;" + eol
    js += "  var listState = [];" + eol
    js += "  var activeCache = [];" + eol
    js += "  let deleted = await " + cache_store + ".clear();" + eol
    js += "  selfr.setState({'compare':false});" + eol
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
    t.NanohubUtils.storageFactory(tp, store_name=store_name)
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
    Component = t.TeleportComponent("Dummy", t.TeleportElement(t.TeleportContent(elementType="container")))
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
                param = t.TeleportElement(t.TeleportContent(elementType="InputChoice"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["options"] = v.get("options", [])
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Integer":
                param = t.TeleportElement(t.TeleportContent(elementType="InputInteger"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["suffix"] = v.get("units", "")
                param.content.attrs["min"] = v.get("min", None)
                param.content.attrs["max"] = v.get("max", None)
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Number":
                param = t.TeleportElement(t.TeleportContent(elementType="InputNumber"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["suffix"] = v.get("units", "")
                param.content.attrs["min"] = v.get("min", None)
                param.content.attrs["max"] = v.get("max", None)
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Text" :
                param = t.TeleportElement(t.TeleportContent(elementType="InputText"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["suffix"] = v.get("units", "")
                param.content.attrs["multiline"] = v.get("multiline", True)
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Tag" :
                param = t.TeleportElement(t.TeleportContent(elementType="InputText"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Boolean":
                param = t.TeleportElement(t.TeleportContent(elementType="InputBoolean"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Dict":
                param = t.TeleportElement(t.TeleportContent(elementType="InputDict"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.List" or v["type"] == "input.Array":
                param = t.TeleportElement(t.TeleportContent(elementType="InputList"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.File":
                param = t.TeleportElement(t.TeleportContent(elementType="InputFile"))
                param.content.attrs["value"] = value
                param.content.attrs["label"] = v.get("label", "")
                param.content.attrs["description"] = v.get("description", "")
                param.content.attrs["accept"] = v.get("accept", "*")
                param.content.attrs["variant"] = v.get("variant", "outlined")
            elif v["type"] == "input.Image":
                param = t.TeleportElement(t.TeleportContent(elementType="InputFile"))
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
    
    NComponent = t.TeleportComponent(
        "AppSettingsComponent",
        t.TeleportElement(m.MaterialContent(elementType="Paper")),
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

    Tabs = a.AppBuilder.createGroups(NComponent, layout, params)
    
    runSimulation = SimtoolBuilder.onSimulate(
        tp,
        NComponent,
        cache_store=kwargs.get("cache_store", "CacheStore"),
        toolname=toolname,
        revision=revision,
        url=url,
        outputs=outputs,
        jupyter_cache=None,
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
    Grid = t.TeleportElement(m.MaterialContent(elementType="Grid"))
    Grid.content.attrs["container"] = True
    Grid.content.attrs["direction"] = "column"

    Text0 = t.TeleportStatic()
    Text0.content = "Simulate"
    ToggleButton0 = t.TeleportElement(m.MaterialContent(elementType="ToggleButton"))
    ToggleButton0.addContent(Text0)
    ToggleButton0.content.attrs["selected"] = True
    ToggleButton0.content.style = {"width":"inherit"}
    ToggleButton0.content.events['click'] = runSimulation
    ToggleButton0.content.attrs["value"] = "runSimulation"

    ToggleButton1 = t.TeleportElement(m.MaterialContent(elementType="ToggleButton"))
    ToggleButton1.addContent(Text0)
    ToggleButton1.content.attrs["selected"] = True
    ToggleButton1.content.style = {"width":"inherit"}
    ToggleButton1.content.events['click'] = runSimulation
    ToggleButton1.content.attrs["value"] = "runSimulation"

    
    Tabs.addContent(Grid)

    Gridt = t.TeleportElement(m.MaterialContent(elementType="Grid"))
    Gridt.content.attrs["color"] = "secondary"
    Gridt.content.attrs["container"] = True
    Gridt.content.attrs["direction"] = "column"
    resetv = []
    resetv = [{ "type": "stateChange", "modifies": k,"newState": v["default_value"]}
        for k,v in parameters.items()
    ]
    resetv.append({
        'type': 'propCall2',
        'calls': 'onChange',
        'args': [json.dumps(parameters)]
    })

    Buttontt = t.TeleportElement(m.MaterialContent(elementType="ToggleButton"))
    Buttontt.addContent(t.TeleportStatic(content="Restore Default Parameters"))
    Buttontt.content.attrs["selected"] = True
    Buttontt.content.attrs["value"] = "Restore"
    Buttontt.content.style = {
        'backgroundColor':'#999999', 
        'color':'rgba(255, 255, 255, 0.87)',
        'width':'inherit'
    }
    Buttontt.content.events['click'] = resetv

    onCleanCache = cleanCache(tp, NComponent)  

    Buttontc = t.TeleportElement(m.MaterialContent(elementType="ToggleButton"))
    Buttontc.addContent(t.TeleportStatic(content="Purge Cached Results"))
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

def AppBar(*args, **kwargs):
    AppBar = t.TeleportElement(m.MaterialContent(elementType="AppBar"))
    AppBar.content.attrs["position"] = "static"
    AppBar.content.attrs["color"] = kwargs.get("color", "primary")
    AppBar.content.style = {"width": "inherit"}

    ToolBar = t.TeleportElement(m.MaterialContent(elementType="Toolbar"))
    ToolBar.content.attrs["variant"] = kwargs.get("variant", "regular")

    Typography = t.TeleportElement(m.MaterialContent(elementType="Typography"))
    Typography.content.attrs["variant"] = "h6"
    Typography.content.style = {"flex": 1, "textAlign": "center"}
    TypographyText = t.TeleportStatic(content=kwargs.get("title", ""))
    Typography.addContent(TypographyText)
    
    ToolBar.addContent(Typography)
    AppBar.addContent(ToolBar)
    return AppBar


def Results(*args, **kwargs):
    results = kwargs.get("results", {})
    onClick = kwargs.get("onClick", [])
    onLoad = kwargs.get("onLoad", [])
    ToggleButtonGroup = t.TeleportElement(
        m.MaterialContent(elementType="ToggleButtonGroup")
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
        ToggleButton = t.TeleportElement(
            m.MaterialContent(elementType="ToggleButton")
        )
        ToggleButton.content.attrs["value"] = k
        ToggleButton.content.events["click"] = onClick + v_action + onLoad
        Typography = t.TeleportElement(m.MaterialContent(elementType="Typography"))
        Typography.addContent(t.TeleportStatic(content=v["title"]))
        ToggleButton.addContent(Typography)
        ToggleButtonGroup.addContent(ToggleButton)

    return ToggleButtonGroup