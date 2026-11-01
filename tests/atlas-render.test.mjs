import test from 'node:test';
import assert from 'node:assert/strict';

test('all seven atlas sections render scientific SVGs and respond to controls',async()=>{
  const handlers={}, elements=new Map();
  globalThis.location={hash:'#b1'};
  globalThis.window={addEventListener:(key,fn)=>{handlers[key]=fn;},scrollTo:()=>{}};
  globalThis.document={
    getElementById:(id)=>{
      if(!elements.has(id))elements.set(id,{innerHTML:'',classList:{toggle(){}}});
      return elements.get(id);
    },
    querySelectorAll:()=>[],
    querySelector:()=>({value:'',disabled:false}),
    addEventListener:(key,fn)=>{handlers[key]=fn;}
  };
  try{
    await import('../docs/lab/app.mjs');
    for(const id of ['b1','t1','t2','t3','t4','t5','t6']){
      globalThis.location.hash='#'+id;
      handlers.hashchange();
      const main=elements.get('main')?.innerHTML||'';
      const visual=elements.get('viz')?.innerHTML||'';
      assert.ok(main.includes('Laboratório interativo'),id+' missing educational panel');
      assert.ok(main.includes('Formulação'),id+' missing formula');
      assert.ok(main.includes('Definições mínimas'),id+' missing definitions');
      assert.ok(visual.includes('<svg'),id+' missing SVG');
      assert.ok(!visual.includes('Falha na visualização'),id+' visualization failed');
    }
    globalThis.location.hash='#b1';handlers.hashchange();
    const before=elements.get('viz').innerHTML;
    handlers.click({target:{closest(selector) {
      return selector==='[data-cell]'?{dataset:{cell:'0,2'}}:null;
    }}});
    assert.notEqual(elements.get('viz').innerHTML,before,'B1 cell toggle did not update chart');
    globalThis.location.hash='#t1';handlers.hashchange();
    const beforeT=elements.get('viz').innerHTML;
    handlers.input({target:{dataset:{param:'lambda'},value:'2.9',type:'range'}});
    assert.notEqual(elements.get('viz').innerHTML,beforeT,'T1 slider did not update chart');
  }finally{
    delete globalThis.location;delete globalThis.window;delete globalThis.document;
  }
});
