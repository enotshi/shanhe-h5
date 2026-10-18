import {parseHTML} from 'linkedom';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
const project=fileURLToPath(new URL('../',import.meta.url));
const {window, document}=parseHTML(await readFile(project+'/site/index.html','utf8'));
const state={width:1440,height:900,y:0};
const sectionTops=[0,1100,2100,3100,4100,5100,6100,7300];
Object.assign(globalThis,{window,document,location:{hash:''}});
Object.defineProperties(globalThis,{
 innerHeight:{get:()=>state.height,configurable:true},
 scrollY:{get:()=>state.y,configurable:true}
});
globalThis.matchMedia=query=>({
 matches:query.includes('reduced-motion')?false:query.includes('max-width: 1023')?state.width<=1023:false,
 addEventListener:()=>{}
});
globalThis.getComputedStyle=el=>({
 position:el.classList?.contains('map-panel')?'sticky':'static',
 getPropertyValue:()=>state.width<768?'60px':'68px'
});
globalThis.requestAnimationFrame=fn=>setTimeout(fn,0);
const root=document.documentElement;
Object.defineProperty(root,'scrollHeight',{get:()=>8500});
document.querySelectorAll('[data-chapter]').forEach((el,i)=>{
 el.getBoundingClientRect=()=>({top:sectionTops[i]-state.y,bottom:sectionTops[i]+700-state.y});
});
const map=document.querySelector('#route-map');
map.getBoundingClientRect=()=>({width:state.width<768?350:600,height:state.width<768?280:480});
document.querySelector('.map-panel').getBoundingClientRect=()=>{
 const top=Math.max(state.width<768?60:90,1000-state.y);
 return {top,bottom:top+(state.width<768?330:700)};
};
const dialog=document.querySelector('#reader-dialog');
Object.defineProperty(dialog,'open',{get(){return this.hasAttribute('open')}});
dialog.showModal=function(){this.setAttribute('open','')};
dialog.close=function(){this.removeAttribute('open');this.dispatchEvent(new window.Event('close'))};
dialog.getBoundingClientRect=()=>({top:0,bottom:800,left:0,right:600});
await import(project+'/site/app.js');
const wait=()=>new Promise(r=>setTimeout(r,15));
async function scroll(y){state.y=y;window.dispatchEvent(new window.Event('scroll'));await wait();}
assert.equal(root.dataset.chapter,'P0');
await scroll(1200);
assert.equal(root.dataset.chapter,'P1');
assert.equal(map.querySelectorAll('[data-route="march"][data-segment].is-shown').length,2);
assert.equal(map.querySelector('[data-node="shanghai"]').classList.contains('is-visible'),false);
await scroll(2200);assert.equal(root.dataset.chapter,'P2');
assert.equal(map.querySelectorAll('[data-route="march"][data-segment].is-shown').length,7);
await scroll(3200);assert.equal(root.dataset.chapter,'P3');
assert.equal(map.querySelector('[data-huining]').classList.contains('is-visible'),true);
await scroll(4200);assert.equal(root.dataset.chapter,'P4');
assert.equal(map.querySelector('[data-node="shanghai"]').classList.contains('is-visible'),true);
await scroll(5200);assert.equal(root.dataset.chapter,'P5');
assert.equal(map.querySelectorAll('[data-route="west"][data-segment].is-shown').length,5);
await scroll(6200);assert.equal(root.dataset.chapter,'P6');
assert.equal(map.querySelector('[data-node="xian"]').classList.contains('is-current'),true);
await scroll(7400);assert.equal(root.dataset.chapter,'P7');
await scroll(1200);assert.equal(root.dataset.chapter,'P1');
assert.equal(map.querySelectorAll('[data-route="west"][data-segment].is-shown').length,0);
const detail=document.querySelector('a[data-detail="ferry"]');
detail.dispatchEvent(new window.Event('click',{bubbles:true,cancelable:true}));
assert.equal(dialog.open,true);
assert.match(document.querySelector('#dialog-title').textContent,/南京/);
assert.ok(dialog.querySelector('img[src="./assets/ferry.svg"]'));
document.querySelector('[data-close-dialog]').dispatchEvent(new window.Event('click',{bubbles:true}));
assert.equal(dialog.open,false);
const source=document.querySelector('[data-source="S8"]');
source.dispatchEvent(new window.Event('click',{bubbles:true,cancelable:true}));
assert.equal(dialog.open,true);assert.match(dialog.textContent,/1956年9月10日/);dialog.close();
document.querySelector('[data-open-toc]').dispatchEvent(new window.Event('click',{bubbles:true}));
assert.equal(dialog.querySelectorAll('.dialog-toc a').length,8);dialog.close();
for (const photo of document.querySelectorAll('[data-photo]')) {
 photo.dispatchEvent(new window.Event('click',{bubbles:true,cancelable:true}));
 assert.equal(dialog.open,true);
 assert.ok(dialog.querySelector('.lightbox-figure img'));
 assert.ok(dialog.querySelector('a[target="_blank"]'));
 dialog.close();
}
assert.equal(document.querySelectorAll('[data-photo]').length,4);
assert.ok(map.querySelectorAll('[data-province]').length>15);
assert.match(document.querySelector('.letter-card').textContent,/四所交通大学/);
assert.match(document.querySelector('.letter-card blockquote').textContent,/聚焦国家重大战略需求/);
assert.equal(document.querySelector('.map-caption').textContent.includes('无行政底图'),false);
state.width=390;state.height=844;await scroll(0);
window.dispatchEvent(new window.Event('resize'));await wait();
assert.equal(root.dataset.chapter,'P0','Mobile hero should not skip to chapters before map is pinned');
await scroll(1200);assert.equal(root.dataset.chapter,'P1');
const radius=Number(map.querySelector('.touch-target').getAttribute('r'));
assert.ok(radius*2*Math.min(350/1000,280/800)>=43.9);
console.log('PASS: 8 chapter states, reverse scroll, mobile hero/pinned map, touch geometry, ferry/source/TOC dialogs, 4 photo lightboxes, province background and verified letter section.');
console.log('DOM emulation only; no browser layout, native focus-trap, visual, or real-device claims.');
