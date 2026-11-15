// Run in CI with the pinned Playwright installation supplied in the environment.
// The authoring environment cannot launch Chromium; this is an independent
// render/interaction gate, not a claim that local visual inspection succeeded.
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
import {pathToFileURL} from 'node:url';

if(!process.env.CDKA_PLAYWRIGHT_PATH)throw new Error('Set CDKA_PLAYWRIGHT_PATH to the installed playwright/index.mjs');
const {chromium}=await import(pathToFileURL(process.env.CDKA_PLAYWRIGHT_PATH).href);
const root=process.cwd(),out=resolve(process.argv[2]||'browser-smoke');
const startupCertificate=JSON.parse(await readFile(resolve(root,'docs/data/optional-startup-results.json'),'utf8'));
const expectedStartup=(g,w,i,objective)=>startupCertificate.cases.find(point=>point.prices.gate===g&&point.prices.write===w&&point.prices.setup===i)[objective];
await mkdir(out,{recursive:true});
const mime={'.html':'text/html; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.css':'text/css; charset=utf-8'};
const server=createServer(async(req,res)=>{
 try{
  const path=resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
  if(!path.startsWith(root+sep)){res.writeHead(403);res.end();return;}
  const body=await readFile(path);res.writeHead(200,{'content-type':mime[extname(path)]||'application/octet-stream'});res.end(body);
 }catch{res.writeHead(404);res.end('Not found');}
});
await new Promise(done=>server.listen(0,'127.0.0.1',done));
let browser;
const report={viewports:[],controls:[],page_errors:[]};
try{
 browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width:1360,height:1100}});
 page.on('pageerror',e=>report.page_errors.push(e.message));
 await page.goto(`http://127.0.0.1:${server.address().port}/docs/lab/shared_budget.html`);
 await page.waitForFunction(()=>document.getElementById('status')?.textContent.startsWith('Dados carregados'),undefined,{timeout:15000});
 assert.equal(await page.locator('#references tr').count(),6);
 assert.equal(await page.locator('#startup-references tr').count(),4);
 assert.equal(await page.locator('#startup-references tr.startup-analytic').count(),1);
 assert.match(await page.locator('#startup-blind-detail').textContent(),/Diagnóstico inicial: 0 quanta; NANDs de seleção: 0/);
 assert.equal(await page.locator('svg').count(),2);
 assert.ok(await page.getByText('Uso causal verificado:',{exact:true}).isVisible());
 await page.screenshot({path:resolve(out,'desktop.png'),fullPage:true});
 for(const [g,w,i,objective] of [[0,6,0,'tasks'],[0,6,6,'cycles'],[1,6,6,'tasks'],[2,24,6,'cycles']]){
  await page.selectOption('#gate-price',String(g));await page.selectOption('#write-price',String(w));
  await page.selectOption('#setup-price',String(i));await page.selectOption('#objective',objective);
  const gain=await page.locator('#gain').textContent();
  assert.equal(gain.startsWith('0,000000'),g>0);
  const startup=await page.locator('#startup-blind-gap').textContent();
  const channel=await page.locator('#startup-channel-effect').textContent();
  assert.match(startup,/p\.p\.$/);assert.match(channel,/p\.p\.$/);
  const certified=expectedStartup(g,w,i,objective);
  assert.equal(await page.locator('#startup-blind-gap').getAttribute('title'),certified.physical_gap_over_optional_blind.exact);
  assert.equal(await page.locator('#startup-channel-effect').getAttribute('title'),certified.reoptimized_all_channel_effect.exact);
  assert.match(await page.locator('#startup-references tr').last().textContent(),/intervenção analítica/);
  report.controls.push({g,w,i,objective,gain,startup_blind_gap:startup,all_channel_effect:channel});
 }
 // Exercise free and paid acquisition while reading exact same-case values;
 // the browser cannot substitute a different horizon or a historical gain.
 await page.selectOption('#gate-price','0');await page.selectOption('#write-price','0');await page.selectOption('#setup-price','0');await page.selectOption('#objective','tasks');
 assert.equal(await page.locator('#startup-blind-gap').getAttribute('title'),expectedStartup(0,0,0,'tasks').physical_gap_over_optional_blind.exact);
 await page.selectOption('#write-price','6');
 assert.equal(await page.locator('#startup-blind-gap').getAttribute('title'),expectedStartup(0,6,0,'tasks').physical_gap_over_optional_blind.exact);
 assert.equal(await page.locator('#startup-channel-effect').getAttribute('title'),expectedStartup(0,6,0,'tasks').reoptimized_all_channel_effect.exact);
 await page.selectOption('#gate-price','1');await page.selectOption('#write-price','6');await page.selectOption('#objective','tasks');
 await page.locator('#balance').focus();await page.keyboard.press('End');
 for(let i=0;i<12;i++)await page.keyboard.press('ArrowLeft');
 assert.equal(await page.locator('#balance-value').textContent(),'84');
 assert.match(await page.locator('#fresh-trace-content').textContent(),/resource:write/);
 assert.match(await page.locator('#elide-trace-content').textContent(),/resource:enable/);
 for(const width of [1360,390,328]){
  await page.setViewportSize({width,height:950});
  const dimensions=await page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth}));
  assert.ok(dimensions.scroll<=dimensions.viewport+1,JSON.stringify(dimensions));
  assert.ok(await page.locator('#references').isVisible());
  assert.ok(await page.locator('#startup-references').isVisible());
  report.viewports.push(dimensions);
  await page.screenshot({path:resolve(out,`width-${width}.png`),fullPage:true});
 }
 assert.deepEqual(report.page_errors,[]);
 report.passed=true;
}finally{
 await writeFile(resolve(out,'report.json'),JSON.stringify(report,null,2)+'\n');
 await browser?.close();await new Promise(done=>server.close(done));
}
console.log(JSON.stringify(report));
