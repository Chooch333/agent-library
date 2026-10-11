// R&D lab reference, 2026-10-11. Not production code. Starting point for TH's arch-renders generator.
// What it is: the script that wrote the Crider & Crider (250510) scene file loaded into Pascal on Charles's PC in round 2.
// Target: Pascal runtime / @pascal-app/core 1.0.3 (the one-command install). Repo main uses a different wall-finish format
//   (slots {a,b} + faceRegions); 1.0.3 uses slots {exterior, interior, lower/middle/upper/topExterior+Interior} + faceBands.
//   Zod drops unknown keys silently, so a wrong-version file loads with finishes missing.
// Dimensions are hard-coded from the six Crider sheets (A300 finish schedule, plans). TH replaces them with takeoff.json.
// Output: {graph:{nodes, rootNodeIds, collections, materials}, counts}. 56 walls, 58 windows, 1 door, 5 blocks, flat roof, 2 slabs.
// Use: run as a browser/Node expression, JSON.stringify(result.graph), validate each node with core 1.0.3 AnyNode.safeParse,
//   then load in Pascal via Settings > Load build ("Replace current scene").
// Known gotchas: doorCategory allows only 'interior' or 'garage'; window position = [distance along wall, sill + h/2, 0];
//   corners: long faces extend +/- half thickness, short faces inset by half thickness + 0.02 m.
// Materials: 1.0.3 has no siding IDs; wood -> wood-woodplank48, rib -> preset-charcoal (as loaded on the PC).
(()=>{
const ft=(f,i=0)=>Math.round((f+i/12)*0.3048*1e4)/1e4, r4=v=>Math.round(v*1e4)/1e4;
const rid=p=>p+'_'+Array.from({length:16},()=>'abcdefghijklmnopqrstuvwxyz0123456789'[Math.floor(Math.random()*36)]).join('');
const M={brick:'library:flooring-rusticbrick',stone:'library:flooring-wallstone1',eifs:'library:concrete-stucco',acm:'library:preset-lightgrey',acm2:'library:preset-charcoal',wood:'library:wood-woodplank48',canopy:'library:preset-charcoal',coping:'library:preset-midgrey',rib:'library:preset-charcoal',cap:'library:concrete-raw',frame:'#1c1c1c'};
const W=ft(128,8),D=ft(63,8),T=ft(1,2),hh=T/2,g0=hh+0.02,N={};
const add=n=>(N[n.id]=n,n);
const base=(t,parent,kw)=>Object.assign({object:'node',id:rid(t==='roof-segment'?'rseg':t),type:t,parentId:parent,visible:true,metadata:{}},kw);
const site=add(base('site',null,{polygon:{type:'polygon',points:[[-25,-25],[65,-25],[65,45],[-25,45]]},children:[]}));
const bld=add(base('building',site.id,{children:[],position:[0,0,0],rotation:[0,0,0]}));site.children.push(bld.id);
const level=(name,i,h,meta)=>{const L=add(base('level',bld.id,{name,children:[],level:i,baseElevation:0,height:h}));L.metadata=meta||{label:name};bld.children.push(L.id);return L;};
const L1=level('First Level',0,ft(14)),L2=level('Second Level',1,ft(14)),RL=level('Roof',2,0.2,{role:'roof',label:'Roof',referenceLevelId:null});RL.metadata.referenceLevelId=L2.id;
for(const L of [L1,L2]){const s=add(base('slab',L.id,{name:L.name+' slab',polygon:[[0,0],[W,0],[W,D],[0,D]],holes:[],holeMetadata:[],elevation:0.1,thickness:0.1,recessed:false,autoFromWalls:false}));s.metadata={role:'story-slab'};L.children.push(s.id);}
const bay=(len,wins)=>({kind:'bay',len,wins});
const longFace=entry=>{const s=[{kind:'pier',len:ft(4)},bay(ft(21,4),[{c:ft(4,8),w:ft(8)},{c:ft(21,4)-ft(4,8),w:ft(8)}]),{kind:'pier',len:ft(3,4),raise:1},
 bay(ft(21,8),[{c:ft(4,8),w:ft(8)},{c:ft(21,8)-ft(4,8),w:ft(8)}]),{kind:'pier',len:ft(3,4),raise:1},bay(ft(21,8),[{c:ft(4,8),w:ft(8)},{c:ft(21,8)-ft(4,8),w:ft(8)}]),
 {kind:'pier',len:ft(3,4),raise:1},{kind:'wood',len:ft(3,4),raise:1},{kind:entry,len:ft(18,4)},{kind:'tower',len:W-ft(100,4),wins:[{c:ft(9,4),w:ft(6,6)},{c:ft(19),w:ft(6,6)}]}];
 s[3].raise=1;s[5].raise=1;s[0].len+=hh;s[s.length-1].len+=hh;return s;};
const shortBay=l=>bay(l,[{c:ft(4,2),w:ft(6)},{c:l-ft(4,2),w:ft(6)}]);
const faces={east:{start:[-hh,D],dir:[1,0],segs:longFace('entry')},west:{start:[-hh,0],dir:[1,0],segs:longFace('m2')},
 south:{start:[0,g0],dir:[0,1],segs:[{kind:'pier',len:ft(3,8)-g0},shortBay(ft(16,8)),{kind:'pier',len:ft(3,4)},shortBay(ft(16,8)),{kind:'pier',len:ft(3,4)},shortBay(ft(16,8)),{kind:'pier',len:D-ft(60,4)-g0}]},
 north:{start:[W,g0],dir:[0,1],segs:[{kind:'tower',len:D-2*g0,wins:[{c:ft(12)-g0,w:ft(6,6)},{c:ft(32)-g0,w:ft(6,6)},{c:ft(52)-g0,w:ft(6,6)}]}]}};
function spec(lv,s){const up=lv==='L2',H=up?(s.raise?ft(18,8):ft(17,4)):ft(14),k=s.kind;let bands=[M.brick],hts=[],wins=[],door=null;
 const ws=(sill,h)=>(s.wins||[]).map(w=>({...w,sill,h}));
 if(!up){ if(k==='pier'||k==='wood')bands=[M.brick];
  else if(k==='bay'){bands=[M.eifs,M.acm,M.eifs,M.stone];hts=[ft(2),ft(7,4),ft(1,8)];wins=ws(ft(2),ft(7));}
  else if(k==='entry'){const L=s.len;bands=[M.acm2,M.stone];hts=[ft(12,6)];wins=[{c:ft(3,6),w:ft(5),sill:0.02,h:ft(8,6)},{c:L-ft(3,6),w:ft(5),sill:0.02,h:ft(8,6)},{c:L/2,w:ft(6),sill:ft(9,4),h:ft(3)}];door={c:L/2,w:ft(6),h:ft(8)};}
  else if(k==='m2'){const L=s.len;bands=[M.acm2];wins=[{c:L*.28,w:ft(6),sill:ft(2),h:ft(7)},{c:L*.72,w:ft(6),sill:ft(2),h:ft(7)}];}
  else {bands=[M.brick];wins=ws(ft(2),ft(7));}
 } else {
  if(k==='pier'||k==='wood'){bands=[M.stone,M.wood,M.acm];hts=[ft(1,6),ft(12,6)];}
  else if(k==='bay'){bands=[M.stone,M.acm,M.eifs,M.acm];hts=[ft(1,6),ft(7,10),ft(2)];wins=ws(ft(1,6),ft(7,6));}
  else if(k==='entry'){bands=[M.acm2];wins=[{c:s.len/2,w:s.len-ft(3),sill:ft(1),h:ft(11)}];}
  else if(k==='m2'){const L=s.len;bands=[M.acm2];wins=[{c:L*.28,w:ft(6),sill:ft(1,6),h:ft(7,6)},{c:L*.72,w:ft(6),sill:ft(1,6),h:ft(7,6)}];}
  else {bands=[M.brick,M.rib,M.cap];hts=[ft(14),ft(2,10)];wins=ws(ft(1,6),ft(7,6));}
 } return {H,bands,hts,wins,door};}
function wallFinish(sp){const n=sp.bands.length,slots={exterior:sp.bands[n-1],interior:sp.bands[n-1]};if(n===1)return {slots};
 const names=n===2?['lower','upper']:n===3?['lower','middle','upper']:['lower','middle','upper','top'];
 names.forEach((nm,i)=>{slots[nm+'Exterior']=sp.bands[i];slots[nm+'Interior']=sp.bands[i];});
 const fb={enabled:true,count:n,lowerHeight:sp.hts[0]??0.84,middleHeight:sp.hts[1]??0.61,upperHeight:sp.hts[2]??0.61};
 return {slots,faceBands:fb};}
const WIN={constructionType:'framed',dimensionReference:'nominal',openingKind:'window',windowType:'fixed',operationState:0,awningDirection:'up',casementStyle:'single',hingesSide:'left',openingShape:'rectangle',openingRadiusMode:'all',openingCornerRadii:[0.15,0.15,0.15,0.15],cornerRadius:0.15,archHeight:0.35,openingRevealRadius:0.025,frameThickness:0.06,frameDepth:0.07,columnDividerThickness:0.045,rowDividerThickness:0.045,sill:true,sillDepth:0.08,sillThickness:0.03};
const DOOR={constructionType:'framed',dimensionReference:'nominal',doorCategory:'interior',doorType:'hinged',leafCount:2,operationState:0,slideDirection:'left',trackStyle:'none',garagePanelCount:4,openingKind:'door',openingShape:'rectangle',openingRadiusMode:'all',openingTopRadii:[0.15,0.15],cornerRadius:0.15,archHeight:0.45,openingRevealRadius:0.025,frameThickness:0.05,frameDepth:0.07,threshold:true,thresholdHeight:0.02,hingesSide:'left',swingDirection:'outward',swingAngle:0,segments:[{type:'panel',heightRatio:0.4,columnRatios:[1],dividerThickness:0.03,panelDepth:0.01,panelInset:0.04},{type:'panel',heightRatio:0.6,columnRatios:[1],dividerThickness:0.03,panelDepth:0.01,panelInset:0.04}],handle:true,handleHeight:1.05,handleSide:'right',contentPadding:[0.04,0.04],doorCloser:false,panicBar:false,panicBarHeight:1};
const counts={walls:0,windows:0,doors:0,blocks:0};
for(const [lv,L] of [['L1',L1],['L2',L2]]) for(const [fname,f] of Object.entries(faces)){let pos=0;
 for(const s of f.segs){const a=[r4(f.start[0]+f.dir[0]*pos),r4(f.start[1]+f.dir[1]*pos)];pos+=s.len;const e=[r4(f.start[0]+f.dir[0]*pos),r4(f.start[1]+f.dir[1]*pos)];
  const sp=spec(lv,s);const w=add(base('wall',L.id,{name:`${lv} ${fname} ${s.kind}`,children:[],thickness:T,height:r4(sp.H),start:a,end:e,...wallFinish(sp),frontSide:'unknown',backSide:'unknown'}));
  L.children.push(w.id);counts.walls++;
  for(const wn of sp.wins){const n=add(base('window',w.id,{position:[r4(wn.c),r4(wn.sill+wn.h/2),0],rotation:[0,0,0],wallId:w.id,width:r4(wn.w),height:r4(wn.h),columnRatios:wn.w>ft(7)?[1,1,1,1]:[1,1,1],rowRatios:wn.h>ft(9)?[1,1,1,1,1]:[1,1,1,1],slots:{frame:M.frame},...WIN}));w.children.push(n.id);counts.windows++;}
  if(sp.door){const d=add(base('door',w.id,{position:[r4(sp.door.c),r4(sp.door.h/2),0],rotation:[0,0,0],wallId:w.id,width:r4(sp.door.w),height:r4(sp.door.h),...DOOR}));w.children.push(d.id);counts.doors++;}
 }}
const box=(wd,ht,dp)=>{const a=wd/2,c=dp/2,v=[[-a,0,-c],[a,0,-c],[a,0,c],[-a,0,c],[-a,ht,-c],[a,ht,-c],[a,ht,c],[-a,ht,c]];
 const E=[['v0','v1'],['v1','v2'],['v2','v3'],['v3','v0'],['v4','v5'],['v5','v6'],['v6','v7'],['v7','v4'],['v0','v4'],['v1','v5'],['v2','v6'],['v3','v7']];
 const F=[['f-bottom',['v0','v1','v2','v3']],['f-top',['v4','v7','v6','v5']],['f-front',['v0','v4','v5','v1']],['f-right',['v1','v5','v6','v2']],['f-back',['v2','v6','v7','v3']],['f-left',['v3','v7','v4','v0']]];
 return {vertices:v.map((p,i)=>({id:'v'+i,position:p.map(r4)})),edges:E.map((e,i)=>({id:'e'+i,vertexIds:e})),faces:F.map(([id,vv])=>({id,vertexIds:vv,materialSlot:'body'}))};};
const block=(L,name,pos,dims,slot)=>{const n=add(base('block',L.id,{name,children:[],position:pos.map(r4),rotation:0,topology:box(...dims),slots:{body:slot},slotNames:{body:'Body'}}));L.children.push(n.id);counts.blocks++;};
for(const side of [1,-1]){const zf=side>0?D+hh:-hh,p=ft(4);block(L2,'M3 canopy '+(side>0?'east':'west'),[ft(41),ft(14),zf+side*p/2],[ft(82),ft(1,6),p],M.canopy);
 if(side>0){let x=ft(4);for(const ln of [ft(21,4),ft(21,8),ft(21,8)]){block(L1,'steel canopy',[x+ln/2,ft(9,1),zf+ft(1,6)],[ln-ft(1),ft(0,4),ft(3)],M.canopy);x+=ln+ft(3,4);}}}
const roof=add(base('roof',RL.id,{name:'Roof',position:[W/2,0,D/2],rotation:0,support:{kind:'level'},children:[]}));roof.metadata={referenceLevelId:L2.id,roofLevelId:RL.id};RL.children.push(roof.id);
const rs=add(base('roof-segment',roof.id,{position:[0,0,0],rotation:0,roofType:'flat',width:W,depth:D,trim:{left:0,right:0,front:0,back:0,frontLeft:0,frontRight:0,backLeft:0,backRight:0,frontLeftX:0,frontLeftZ:0,frontRightX:0,frontRightZ:0,backLeftX:0,backLeftZ:0,backRightX:0,backRightZ:0},wallHeight:0,pitch:0,wallThickness:0.16,deckThickness:0.1,overhang:0,shingleThickness:0.05,managedByParent:false,wallShell:'auto',shedInsetEndPanels:false,gambrelLowerWidthRatio:0.5,gambrelLowerHeightRatio:0.6,mansardSteepWidthRatio:0.15,mansardSteepHeightRatio:0.7,dutchHipWidthRatio:0.25,dutchHipHeightRatio:0.5,dutchWaistLengthRatio:0.98,dutchGabletRake:0.48,dutchTopRakeThickness:0.21,children:[]}));roof.children.push(rs.id);
return {graph:{nodes:N,rootNodeIds:[site.id],collections:{},materials:{}},counts};
})()
