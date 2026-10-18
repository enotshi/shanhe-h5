import {chapters, details, sources, photos} from './data.js';
import {siteConfig} from './config.js';

const root = document.documentElement;
root.classList.add('js');
const map = document.querySelector('#route-map');
const observed = [...document.querySelectorAll('[data-chapter]')];
const navLinks = [...document.querySelectorAll('[data-nav]')];
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const dialog = document.querySelector('#reader-dialog');
const dialogTitle = document.querySelector('#dialog-title');
const dialogBody = document.querySelector('#dialog-body');
let activeId = null;
let raf = 0;
let returnFocus = null;

function setChapter(id) {
  const chapter = chapters.find(item => item.id === id);
  if (!chapter || activeId === id) return;
  activeId = id;
  root.dataset.chapter = id;
  map.dataset.mode = chapter.mode;
  map.querySelectorAll('[data-segment]').forEach(el => {
    const n = Number(el.dataset.segment);
    const limit = el.dataset.route === 'march' ? chapter.march : chapter.west;
    el.classList.toggle('is-shown', n <= limit);
  });
  map.querySelectorAll('[data-node]').forEach(el => {
    const visible = el.dataset.group === 'march'
      ? Number(el.dataset.order) <= chapter.march
      : chapter.mode !== 'march' && Number(el.dataset.order) <= chapter.west;
    el.classList.toggle('is-visible', visible || chapter.focus.includes(el.dataset.node));
    el.classList.toggle('is-current', chapter.focus.includes(el.dataset.node));
    el.setAttribute('aria-hidden', String(!(visible || chapter.focus.includes(el.dataset.node))));
    el.setAttribute('tabindex', visible || chapter.focus.includes(el.dataset.node) ? '0' : '-1');
  });
  map.querySelector('[data-huining]').classList.toggle('is-visible', chapter.huining);
  document.querySelector('#map-period').textContent = chapter.period;
  document.querySelector('#map-chapter-title').textContent = chapter.title;
  document.querySelector('#map-index').textContent = String(chapters.indexOf(chapter)).padStart(2,'0');
  navLinks.forEach(link => {
    if (link.dataset.nav === id) link.setAttribute('aria-current','step');
    else link.removeAttribute('aria-current');
  });
}

function updateOnScroll() {
  raf = 0;
  // 选用阅读区域顶部附近的最近章节，避免固定地图遮挡造成状态偏移。
  const compact = matchMedia('(max-width: 1023px)').matches;
  const stickyMap = document.querySelector('.map-panel');
  const isSticky = getComputedStyle(stickyMap).position === 'sticky';
  const rect = stickyMap.getBoundingClientRect();
  const headerHeight = Number.parseFloat(getComputedStyle(root).getPropertyValue('--header')) || 68;
  const pinned = isSticky && rect.top <= headerHeight + 4 && rect.bottom > headerHeight + 100;
  const line = compact && pinned ? Math.min(innerHeight * .85, rect.bottom + 70) : innerHeight * .40;
  let candidate = observed[0];
  for (const section of observed) {
    if (section.getBoundingClientRect().top <= line) candidate = section;
  }
  setChapter(candidate.id);
  const max = document.documentElement.scrollHeight - innerHeight;
  const fraction = max > 0 ? Math.min(1,Math.max(0,scrollY/max)) : 0;
  document.querySelector('#reading-progress').style.transform = `scaleX(${fraction})`;
}
function scheduleUpdate() { if (!raf) raf = requestAnimationFrame(updateOnScroll); }

function resizeTouchTargets() {
  const box=map.getBoundingClientRect();
  const scale=Math.min(box.width/1000,box.height/800);
  if (scale>0) map.querySelectorAll('.touch-target').forEach(el=>el.setAttribute('r',String(22/scale)));
}

function sourceLink(id) {
  const source = sources.find(item => item.id === id);
  if (!source) return null;
  const a = document.createElement('a');
  a.href = source.url; a.target = '_blank'; a.rel = 'noopener noreferrer';
  a.textContent = `${source.id} · ${source.title}`;
  return a;
}
function openReader(title, content, trigger) {
  returnFocus = trigger || document.activeElement;
  dialogTitle.textContent = title;
  dialogBody.replaceChildren(...content);
  if (typeof dialog.showModal !== 'function') {
    // 旧浏览器不支持dialog时仍可访问来源，并保留章节中的原始正文。
    location.hash = 'sources'; return;
  }
  if (!dialog.open) dialog.showModal();
  dialogBody.scrollTop = 0;
  dialog.querySelector('.dialog-close').focus();
}
function openDetail(id, trigger) {
  const d = details[id]; if (!d) return;
  const tag = document.createElement('p'); tag.className = 'eyebrow'; tag.textContent = d.eyebrow;
  const nodes = [tag, ...d.paragraphs.map(text => {
    const p = document.createElement('p'); p.textContent = text; return p;
  })];
  if (d.illustration === 'ferry') {
    const figure = document.createElement('figure');
    const img = document.createElement('img'); img.src = './assets/ferry.svg';
    img.alt = '原创线条示意：车厢分节、轮渡过江、接续行程';
    const caption = document.createElement('figcaption'); caption.textContent = '南京轮渡过江：分节、渡江、接续';
    figure.append(img,caption); nodes.push(figure);
  }
  const refs = document.createElement('div'); refs.className = 'detail-sources';
  for (const source of d.sourceIds) { const a = sourceLink(source); if (a) refs.append(a); }
  nodes.push(refs); openReader(d.title,nodes,trigger);
}
function openSources(id, trigger) {
  const items = id ? sources.filter(s => s.id === id) : sources;
  const nodes = items.map(s => {
    const block = document.createElement('div'); block.className = 'source-item';
    const a = sourceLink(s.id); const p = document.createElement('p');
    p.textContent = `${s.publisher}。${s.note}`; block.append(a,p); return block;
  });
  const note = document.createElement('p'); note.className='muted';
  note.textContent='沿着文字与影像，重访两段历史。图片出处见各图图注与原文链接。';
  nodes.push(note); openReader(id ? '本段史料依据' : '史料与素材来源',nodes,trigger);
}

document.addEventListener('click', event => {
  const picture = event.target.closest('[data-photo]');
  if (picture) {
    const item=photos[picture.dataset.photo];
    if (!item || typeof dialog.showModal !== 'function') return;
    event.preventDefault();
    const figure=document.createElement('figure'); figure.className='lightbox-figure';
    const img=document.createElement('img'); img.src=`./assets/photos/${item.file}`; img.alt=item.caption;
    const caption=document.createElement('figcaption');caption.textContent=item.caption;
    figure.append(img,caption);
    const credit=document.createElement('p');credit.className='photo-credit';credit.textContent=`来源：${item.credit}`;
    const link=document.createElement('a');link.href=item.url;link.target='_blank';link.rel='noopener noreferrer';link.textContent='查看原文 ↗';
    openReader(item.title,[figure,credit,link],picture);return;
  }
  const detail = event.target.closest('[data-detail]');
  if (detail) { event.preventDefault(); openDetail(detail.dataset.detail,detail); return; }
  const source = event.target.closest('[data-source]');
  if (source) { event.preventDefault(); openSources(source.dataset.source || null,source); return; }
  const toc = event.target.closest('[data-open-toc]');
  if (toc) {
    const list = document.createElement('nav'); list.className='dialog-toc';
    chapters.forEach((chapter,index) => {
      const a=document.createElement('a'); a.href=`#${chapter.id}`;
      a.textContent=`${String(index).padStart(2,'0')}　${chapter.title}`;
      a.addEventListener('click',()=>dialog.close()); list.append(a);
    });
    openReader('沿路阅读', [list],toc); return;
  }
  if (event.target.closest('[data-close-dialog]')) dialog.close();
});
dialog.addEventListener('click', event => { if (event.target === dialog) {
  const r=dialog.getBoundingClientRect();
  if (event.clientX<r.left || event.clientX>r.right || event.clientY<r.top || event.clientY>r.bottom) dialog.close();
}});
dialog.addEventListener('close',()=>{ if(returnFocus?.isConnected) returnFocus.focus({preventScroll:true}); });

// 原生dialog负责焦点约束和Esc；SVG链接以Enter激活，按钮支持Space。
window.addEventListener('scroll',scheduleUpdate,{passive:true});
window.addEventListener('resize',()=>{resizeTouchTargets();scheduleUpdate();});
window.addEventListener('hashchange',scheduleUpdate);
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(scheduleUpdate, {threshold:[0,.2,.5,.8,1]});
  observed.forEach(section=>observer.observe(section));
}
document.querySelectorAll('a[href^="#P"]').forEach(a=>a.addEventListener('click',()=>{
  const id = a.getAttribute('href').slice(1); setChapter(id);
}));
if (motion.matches) root.classList.add('reduced-motion');
motion.addEventListener?.('change',e=>root.classList.toggle('reduced-motion',e.matches));
if (siteConfig.author || siteConfig.affiliation) {
  document.querySelector('#author-line').textContent = [siteConfig.author,siteConfig.affiliation].filter(Boolean).join(' · ');
}
resizeTouchTargets();
updateOnScroll();


// 第07部分：将折叠容器改为普通容器，所有设备始终显示。
const recapDetails = document.querySelector("details.route-recap");

if (recapDetails) {
  const staticMap = document.createElement("div");
  staticMap.className = recapDetails.className;

  const heading = document.createElement("div");
  heading.className = "recap-static-heading";
  heading.textContent = "两条道路，一幅山河";
  staticMap.append(heading);

  const content = recapDetails.querySelector(".route-recap-content");
  if (content) {
    staticMap.append(content);
  }

  recapDetails.replaceWith(staticMap);
}