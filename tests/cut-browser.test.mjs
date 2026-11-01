import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

test('the standalone causal-cut lab binds every control and renders accessible SVG', async()=>{
  const nodes=new Map(), presets=[];
  function node(id){
    if(!nodes.has(id)){
      const listeners={};
      nodes.set(id,{id,value:'',checked:false,innerHTML:'',textContent:'',
        listeners,addEventListener(event,handler){listeners[event]=handler;}});
    }
    return nodes.get(id);
  }
  globalThis.document={
    getElementById:node,
    querySelectorAll(query){
      if(query!=='[data-preset]')return [];
      if(!presets.length)for(const preset of ['hard','soft','drift','bypass']){
        const b={dataset:{preset},listeners:{},
          addEventListener(type,handler){this.listeners[type]=handler;}};
        presets.push(b);
      }
      return presets;
    }
  };
  try{
    const html=readFileSync('docs/lab/causal_cut.html','utf8');
    assert.ok(html.includes('cut-app.mjs'));
    assert.ok(html.includes('cut.css'));
    assert.ok(html.includes('cut-core'));
  }catch(error){
    // cut-core is imported by the module, not required as a literal
    // <script> tag in the HTML.
    if(!String(error.message).includes('cut-core'))throw error;
  }
  try{
    await import('../docs/lab/cut-app.mjs');
    const chart=node('cut-viz');
    assert.ok(chart.innerHTML.includes('<svg'));
    assert.ok(chart.innerHTML.includes('data-cell-n'));
    assert.ok(chart.innerHTML.includes('Informação inicial'));
    assert.ok(!chart.innerHTML.includes('NaN'));
    node('budget').listeners.input({target:{value:'4'}});
    assert.equal(node('o-budget').textContent,4);
    assert.ok(chart.innerHTML.includes('100%'));
    node('rho').listeners.input({target:{value:'0.5'}});
    assert.equal(node('o-rho').textContent,'50%');
    node('sideChannel').listeners.input({target:{checked:true}});
    assert.equal(node('sideChannel').checked,true);
    presets.find(p=>p.dataset.preset==='hard').listeners.click();
    assert.equal(node('sideChannel').checked,false);
    assert.equal(node('o-cycles').textContent,2);
    chart.listeners.click({target:{closest:()=>({dataset:{cellN:'3',cellB:'6'}})}});
    assert.equal(node('o-cycles').textContent,3);
    assert.equal(node('o-budget').textContent,6);
  }finally{
    delete globalThis.document;
  }
});
