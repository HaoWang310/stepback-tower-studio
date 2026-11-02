const fs=require('fs'),vm=require('vm'),assert=require('assert');const shell=fs.readFileSync(__dirname+'/shell.html','utf8');const curves=JSON.parse(fs.readFileSync(__dirname+'/curves.json'));const context={console,navigator:{userAgent:"node"}};context.self=context;vm.createContext(context);vm.runInContext(fs.readFileSync(__dirname+'/clipper.js','utf8'),context);const functions=shell.slice(shell.indexOf('const clamp='),shell.indexOf('let scene,camera'));vm.runInContext('const params={floors:[20,20,20],rise:3.6,thickness:.6,step:5,bridgeWidth:.44,attract:.9,randomness:3.6,seed:6};const refs='+JSON.stringify(curves.filter(c=>!c.closed).map(c=>c.points))+';\n'+functions,context);
context.rings=curves.filter(c=>c.closed).map(c=>c.points);vm.runInContext(`
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
if(parseLevels('5,10-12').join(',')!=='5,10,11,12')throw Error('level parsing');
if(parseLevels('0').length||parseLevels('0, 0,').length||parseLevels('0,10').join(',')!=='10')throw Error('zero must disable connections without blocking updates');
let invalid=false;try{parseLevels('12-10')}catch(e){invalid=true}if(!invalid)throw Error('range validation');
for(const r of rings){if(union([r]).length!==1)throw Error('invalid source');const a=towerRing(r,0,5,false),b=towerRing(r,0,6,false);if(eq(a,b))throw Error('random floors repeat');}
const fixedA=rings.map((r,i)=>towerRing(r,i,9,true));params.randomness=7;params.seed=231;const fixedB=rings.map((r,i)=>towerRing(r,i,9,true));if(!eq(fixedA,fixedB))throw Error('connected floors changed with seed or randomness');
for(const f of [9,10]){const rs=rings.map((r,i)=>towerRing(r,i,f,true));const whole=union([...rs,...mst(rs).map(([a,b])=>bridgeRibbon(rs[a],rs[b],.44))]);if(whole.length!==1)throw Error('bridge not unified '+f);}
for(const step of [0,3,8,20,50,100])for(const random of [0,4,8])for(const level of [0,10,19]){params.step=step;params.randomness=random;for(let i=0;i<3;i++){const r=towerRing(rings[i],i,level,false);if(r.flat().some(x=>!Number.isFinite(x)))throw Error('non finite');if(!union([r]).length)throw Error('empty geometry');}}
params.attract=1;params.step=5;params.randomness=4;for(let i=0;i<3;i++){const low=towerRing(rings[i],i,4,false),high=towerRing(rings[i],i,18,false),base=resample(rings[i]);const locked=low.filter((p,j)=>length(sub(p,high[j]))<1e-8&&length(sub(p,base[j]))<1e-8).length;if(locked<12)throw Error('reference facade fails vertical alignment: '+locked);console.log('Aligned facade vertices',i,locked);}
params.randomness=0;for(let i=0;i<3;i++){const baseC=centroid(rings[i]),n=refs.reduce((best,r)=>{const v=nearest(baseC,r);return v.distance<best.distance?v:best},{distance:Infinity}),direction=unit(sub(n.point,baseC));const low=centroid(towerRing(rings[i],i,3,false)),high=centroid(towerRing(rings[i],i,18,false));const advance=dot(sub(high,low),direction);if(advance<=0)throw Error('setback goes away from reference');console.log('Towards-reference centroid advance',i,advance.toFixed(3));}
console.log('PASS: real contours, range validation, independent floor variation, fixed connected floors, whole slab unions, parameter extremes.');
`,context);
const html=fs.readFileSync(__dirname+'/dist/index.html','utf8');assert(!/<(?:script|img)[^>]+src\s*=|<link[^>]+href\s*=/i.test(html),'HTML has external resources');console.log('PASS: standalone HTML has all dependencies and source geometry embedded.');
vm.runInContext(`
params.extraAfter=[5,10];params.extraDistance=6;
for(const [floor,expected] of [[4,0],[5,6],[6,6],[9,6],[10,12],[11,12]])if(extraSetbackAt(floor)!==expected)throw Error('Extra setback triggers on wrong transition');
const sample=[[-30,-20],[30,-20],[30,20],[-30,20]];
for(const distance of [6,12]){const changed=extraSetbackRing(sample,[1,0],distance);if(Math.abs(changed[0][0]-sample[0][0]-distance)>1e-9)throw Error('Extra metres incorrect');if(changed[1][0]!==sample[1][0])throw Error('Opposite side moved');}
params.extraAfter=[];params.extraDistance=0;
console.log('PASS: after-floor triggers, cumulative inheritance, exact extra metres and fixed opposite edge.');
`,context);

// Regression: inspect the whole closed curve, including the last-to-first join.
const curvedContext={console};vm.createContext(curvedContext);vm.runInContext(`const baseModes=['curve'];const params={};const refs=[];`+functions+`

const curvedBase=Array.from({length:128},(_,i)=>{const t=i/128*Math.PI*2;return [30*Math.cos(t),30*Math.sin(t)]});
params.floors=[20];params.step=8;params.randomness=8;refs.splice(0,refs.length,[[30,-30],[38,0],[30,30]]);
for(const attract of [.9,1])for(const seed of [1,6,100])for(const f of [1,10,19]){
params.attract=attract;params.seed=seed;const r=towerRing(curvedBase,0,f,false);
for(let j=0;j<r.length;j++){const u=unit(sub(r[j],r[(j+r.length-1)%r.length])),v=unit(sub(r[(j+1)%r.length],r[j]));if(Math.acos(clamp(dot(u,v),-1,1))>Math.PI/6)throw Error('Abrupt curve turn at '+j+' floor '+f+' count '+r.length+' seed '+seed+' attract '+attract);}
if(r.flat().some(v=>!Number.isFinite(v)))throw Error('Non-finite curve');
}
console.log('PASS: curved setbacks remain smooth at every vertex and the closing seam across attraction and random seeds.');
`,curvedContext);

vm.runInContext(`
params.floors=[20];params.extraAfter=[];params.extraDistance=0;params.randomness=0;params.attract=.9;
const large=[[-30,-30],[30,-30],[30,30],[-30,30]],small=large.map(p=>p.map(v=>v/2));
if(Math.abs(setbackBounds(large,0).maxDepth/2-setbackBounds(small,0).maxDepth)>1e-8)throw Error('Boundary does not scale with footprint');
for(const base of [large,small,rings[0]]){const bounds=setbackBounds(base,0);params.step=100;const limited=towerRing(base,0,19,false);params.step=bounds.maxStrength;const atLimit=towerRing(base,0,19,false);if(JSON.stringify(limited)!==JSON.stringify(atLimit))throw Error('Large strength exceeds automatic boundary');if(bounds.maxDepth>.24*bounds.width+1e-8)throw Error('Depth enters clamped-scale translation regime');}
console.log('PASS: setback boundary scales with footprint and excess strength cannot continue translating upper floors.');
`,context);

// Regression: the facade builder must actually add both trims and respect size.
vm.runInContext(fs.readFileSync(__dirname+'/three.min.js','utf8'),context);
vm.runInContext(shell.slice(shell.indexOf('function addWindowTrims('),shell.indexOf('function setGrowth(')),context);
vm.runInContext(`
const $=()=>({checked:true});const materials=[],warnings=[];
const footprints=[[[-20,-20],[20,-20],[20,20],[-20,20]]];
towerRing=()=>footprints[0];params.floors=[3];params.rise=3.6;params.thickness=.5;params.fasciaHeight=.8;params.glassSetback=.6;params.frameSpacing=3;params.windowTrim=.12;
let floorGroups=[],allPolys=[];
function runFacade(){floorGroups=Array.from({length:3},()=>new THREE.Group());allPolys=Array.from({length:3},()=>({linked:false,polygons:[{outer:footprints[0],holes:[]}]}));addArchitecturalDetails();return floorGroups.flatMap(g=>g.children.filter(m=>m.userData.detail==='trim'));}
let trims=runFacade();if(floorGroups[0].children.some(m=>m.userData.detail==='fascia'))throw Error('Ground slab must have no fascia');if(floorGroups.slice(1).some(g=>!g.children.some(m=>m.userData.detail==='fascia')))throw Error('Upper slab fascia missing');if(trims.length!==4)throw Error('Missing upper/lower trims on window intervals');
if(trims.some(m=>m.geometry.attributes.position.count===0||m.material.color.getHex()!==0x151517))throw Error('Empty trim or wrong color');
if(Math.abs(trims[0].position.z-.5)>1e-8||Math.abs(trims[1].position.z+params.windowTrim-3.45)>1e-8)throw Error('Trim hidden behind fascia');
params.windowTrim=.4;trims=runFacade();if(trims.some(m=>m.userData.detailHeight!==.4))throw Error('Size did not change trim geometry');
params.windowTrim=0;if(runFacade().length)throw Error('Zero must hide trims');
console.log('PASS: facade creates two black window trims, visible between fascia, size changes geometry, zero hides them.');
`,context);
