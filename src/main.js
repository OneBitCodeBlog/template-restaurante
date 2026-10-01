import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const story = document.querySelector('.scroll-story');
const art = document.querySelector('#art-stage');
const wrap = document.querySelector('#canvas-wrap');
const loading = document.querySelector('#loading');
const loadingText = document.querySelector('#loading-text');
const loadingBar = document.querySelector('#loading-bar');
const intro = document.querySelector('.scene-intro');
const detail = document.querySelector('.scene-detail');
const fill = document.querySelector('#progress-fill');
const number = document.querySelector('#progress-number');
const title = document.querySelector('#progress-title');
const caption = document.querySelector('#art-caption-text');
const scrollLabel = document.querySelector('#scroll-label');
const motionPreference = matchMedia('(prefers-reduced-motion: reduce)');
let reducedMotion = motionPreference.matches;
document.documentElement.classList.toggle('reduced-motion', reducedMotion);
const clamp = THREE.MathUtils.clamp;
const mix = THREE.MathUtils.lerp;
const smooth = (a, b, t) => { const v = clamp((t - a) / (b - a), 0, 1); return v * v * (3 - 2 * v); };

let renderer, camera, scene, tray, bite;
let progress = 0, target = 0, frame = 0, previous = 0, loaded = false, visible = true, failed = false;
let lastPhase = -1;
const pointer = new THREE.Vector2();

function failGracefully(error) {
  console.error('A apresentação 3D não pôde ser carregada.', error);
  failed = true;
  document.documentElement.classList.add('no-webgl');
  loading.classList.add('hidden');
  document.querySelector('#fallback').hidden = false;
  wrap.hidden = true;
  document.querySelector('.scroll-invitation').hidden = true;
  document.querySelector('.story-progress').hidden = true;
}

function createModel(gltf, width) {
  const object = gltf.scene;
  const box = new THREE.Box3().setFromObject(object);
  const center = box.getCenter(new THREE.Vector3());
  const size = box.getSize(new THREE.Vector3());
  object.position.sub(center);
  const group = new THREE.Group();
  group.add(object);
  const scale = width / size.x;
  object.scale.setScalar(scale);
  object.position.multiplyScalar(scale);
  const materials = [];
  object.traverse(child => {
    if (!child.isMesh) return;
    const source = Array.isArray(child.material) ? child.material : [child.material];
    source.forEach(material => {
      material.transparent = true;
      material.depthWrite = true;
      material.envMapIntensity = .10;
      material.metalness = 0;
      // The generated roughness map creates glossy patches on the crust.
      // A matte response and gentler normals keep its photographed texture readable.
      material.roughnessMap = null;
      material.roughness = .96;
      if (material.normalMap) material.normalScale.set(.45, .45);
      if (material.map) material.map.anisotropy = Math.min(renderer.capabilities.getMaxAnisotropy(), 8);
      materials.push(material);
    });
  });
  group.userData.materials = materials;
  scene.add(group);
  return group;
}

function opacity(model, value) {
  model.visible = value > .003;
  for (const material of model.userData.materials) {
    material.opacity = value;
    material.depthWrite = value > .98;
  }
}

function resize() {
  if (!renderer) return;
  const { width, height } = art.getBoundingClientRect();
  renderer.setSize(width, height, false);
  renderer.setPixelRatio(Math.min(devicePixelRatio, innerWidth <= 760 ? 1.6 : 2));
  camera.aspect = width / height;
  camera.fov = width / height < .85 ? 43 : 37;
  camera.updateProjectionMatrix();
  updateScroll();
  requestFrame();
}

function updateScroll() {
  const rect = story.getBoundingClientRect();
  target = clamp(-rect.top / Math.max(story.offsetHeight - innerHeight, 1), 0, 1);
  requestFrame();
}

function setCopy(p) {
  const out = reducedMotion ? (p >= .52 ? 1 : 0) : smooth(.43, .57, p);
  const incoming = reducedMotion ? (p >= .52 ? 1 : 0) : smooth(.50, .64, p);
  intro.style.opacity = 1 - out;
  intro.style.transform = `translateY(${-out * 25}px)`;
  detail.style.opacity = incoming;
  detail.style.transform = `translateY(${(1 - incoming) * 25}px)`;
  detail.style.visibility = incoming > 0 ? 'visible' : 'hidden';
  const second = p >= .53;
  intro.inert = second;
  intro.setAttribute('aria-hidden', String(second));
  detail.inert = !second;
  detail.setAttribute('aria-hidden', String(!second));
  const phase = p < .4 ? 0 : p < .7 ? 1 : 2;
  if (lastPhase !== phase) {
    number.textContent = ['01', '02', '03'][phase];
    title.textContent = ['À MESA', 'NOS DETALHES', 'DEU VONTADE?'][phase];
    caption.textContent = phase === 0 ? 'Bons sabores ficam ainda melhores juntos.' : 'Um detalhe que merece toda a atenção.';
    scrollLabel.textContent = phase === 2 ? 'Explore os sabores.' : 'Desça. Abra o apetite.';
    lastPhase = phase;
  }
  fill.style.transform = `scaleX(${Math.max(.02, p)})`;
}

function render(now = 0) {
  frame = 0;
  if (!loaded || !visible || failed) return;
  const dt = previous ? Math.min((now - previous) / 1000, .05) : .016;
  previous = now;
  progress = reducedMotion ? target : mix(progress, target, 1 - Math.exp(-dt * 11));
  if (Math.abs(target - progress) < .0001) progress = target;
  const p = progress;
  const exchange = reducedMotion ? (p >= .52 ? 1 : 0) : smooth(.47, .66, p);
  const flare = reducedMotion ? 0 : Math.sin(exchange * Math.PI);
  // A tighter mobile camera makes both subjects prominent without enlarging the UI.
  const zoom = innerWidth <= 760 ? mix(1.65 - smooth(.15, .42, p) * .34, 1.85, exchange) : 1;
  if (camera.zoom !== zoom) {
    camera.zoom = zoom;
    camera.updateProjectionMatrix();
  }
  document.documentElement.style.setProperty('--progress', p.toFixed(4));
  document.documentElement.style.setProperty('--transition', flare.toFixed(4));
  setCopy(p);

  // Both models share the same visual center; the short light veil hides the change in silhouette.
  const approach = smooth(.29, .57, p);
  tray.rotation.set(.13 + approach * .12, reducedMotion ? -.3 : -.35 + Math.min(p, .62) * 5.4, -.09 + approach * .12);
  tray.scale.setScalar(mix(1, 1.38, approach));
  tray.position.set(-.04 + approach * .05, -.02 - approach * .08, approach * .2);
  opacity(tray, 1 - smooth(0, .78, exchange));

  const reveal = smooth(.49, .8, p);
  bite.rotation.set(.05, reducedMotion ? -.22 : -.55 + smooth(.51, 1, p) * 1.7, mix(-.22, .1, reveal));
  bite.scale.setScalar(mix(.64, 1, reveal));
  bite.position.set(mix(.02, -.01, reveal), mix(-.1, .05, reveal), .22);
  opacity(bite, smooth(.24, 1, exchange));
  if (!reducedMotion) {
    tray.rotation.y += pointer.x * .035;
    bite.rotation.y += pointer.x * .045;
  }
  renderer.render(scene, camera);
  art.dataset.phase = p < .47 ? 'bandeja' : p < .66 ? 'transicao' : 'coxinha';
  art.dataset.progress = p.toFixed(3);
  if (progress !== target) requestFrame();
}

function requestFrame() {
  if (!frame && loaded && visible && !failed) frame = requestAnimationFrame(render);
}

async function init() {
  try {
    renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: 'high-performance' });
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = .82;
    renderer.setClearColor(0x000000, 0);
    renderer.domElement.setAttribute('aria-hidden', 'true');
    wrap.appendChild(renderer.domElement);
    renderer.domElement.addEventListener('webglcontextlost', event => {
      event.preventDefault();
      failGracefully(new Error('WebGL context lost'));
    });
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(37, 1, .1, 100);
    camera.position.set(0, 2.45, 5.6);
    camera.lookAt(0, 0, 0);
    const pmrem = new THREE.PMREMGenerator(renderer);
    const room = new RoomEnvironment();
    const environment = pmrem.fromScene(room, .04);
    scene.environment = environment.texture;
    room.dispose();
    pmrem.dispose();
    // Broad window-like light with a subtle warm tint and soft neutral fill.
    RectAreaLightUniformsLib.init();
    scene.add(new THREE.HemisphereLight(0xfffcf8, 0x302b27, .5));
    const overhead = new THREE.RectAreaLight(0xfff5e8, 2.3, 5, 5);
    overhead.position.set(-3.5, 4, 3);
    overhead.lookAt(0, 0, 0);
    scene.add(overhead);
    const fillLight = new THREE.RectAreaLight(0xffffff, .45, 4, 4);
    fillLight.position.set(3, 1.5, 3);
    fillLight.lookAt(0, 0, 0);
    scene.add(fillLight);
    const loader = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
    const progressByModel = [0, 0];
    const loadModel = (url, i) => loader.loadAsync(url, event => {
      progressByModel[i] = event.total ? event.loaded / event.total : .2;
      const value = Math.round((progressByModel[0] + progressByModel[1]) * 45);
      loadingBar.style.width = `${value}%`;
    });
    const [trayFile, biteFile] = await Promise.all([loadModel('/models/bandeja-v2.glb', 0), loadModel('/models/coxinha.glb', 1)]);
    tray = createModel(trayFile, 3.35);
    bite = createModel(biteFile, 1.48);
    opacity(bite, 0);
    resize();
    await renderer.compileAsync(scene, camera);
    loaded = true;
    art.dataset.loaded = 'true';
    loadingText.textContent = 'A mesa está pronta.';
    loadingBar.style.width = '100%';
    loading.classList.add('hidden');
    progress = target;
    requestFrame();
    new ResizeObserver(resize).observe(art);
    new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; if (visible) requestFrame(); }, { threshold: 0 }).observe(story);
  } catch (error) { failGracefully(error); }
}

addEventListener('scroll', updateScroll, { passive: true });
addEventListener('resize', resize, { passive: true });
art.addEventListener('pointermove', event => {
  if (event.pointerType !== 'mouse' || reducedMotion) return;
  const rect = art.getBoundingClientRect();
  pointer.set((event.clientX - rect.left) / rect.width - .5, (event.clientY - rect.top) / rect.height - .5);
  requestFrame();
});
art.addEventListener('pointerleave', () => { pointer.set(0, 0); requestFrame(); });
document.addEventListener('visibilitychange', () => { visible = !document.hidden; if (visible) requestFrame(); });
motionPreference.addEventListener('change', event => {
  reducedMotion = event.matches;
  document.documentElement.classList.toggle('reduced-motion', reducedMotion);
  updateScroll();
});
document.querySelector('#scroll-invitation').addEventListener('click', () => {
  const distance = Math.max(story.offsetHeight - innerHeight, 1);
  if (target >= .7) { document.querySelector('#sabores').scrollIntoView({ behavior: reducedMotion ? 'instant' : 'smooth' }); return; }
  const next = target < .4 ? .44 : .85;
  scrollTo({ top: story.offsetTop + distance * next, behavior: reducedMotion ? 'instant' : 'smooth' });
});
updateScroll();
init();

const filters = document.querySelectorAll('[data-filter]');
const dishes = document.querySelectorAll('[data-dish]');
filters.forEach(button => button.addEventListener('click', () => {
  const category = button.dataset.filter;
  filters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
  let count = 0;
  dishes.forEach(dish => {
    dish.hidden = category !== 'todos' && dish.dataset.dish !== category;
    if (!dish.hidden) count++;
  });
  document.querySelector('#filter-status').textContent = `${count} ${count === 1 ? "prato" : "pratos"} em ${button.textContent}.`;
}));

// Keep an order action in reach without duplicating the visible hero or closing CTA.
const mobileOrderBar = document.querySelector('.mobile-order-bar');
const orderAnchors = [document.querySelector('#hero-order'), document.querySelector('.delivery-section .order-button')];
const orderVisibility = new Map(orderAnchors.map(element => [element, true]));
const orderObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => orderVisibility.set(entry.target, entry.isIntersecting));
  const show = ![...orderVisibility.values()].some(Boolean);
  mobileOrderBar.classList.toggle('is-visible', show);
  mobileOrderBar.inert = !show;
  mobileOrderBar.setAttribute('aria-hidden', String(!show));
}, { threshold: 0 });
orderAnchors.forEach(element => orderObserver.observe(element));

// Reveals remain progressive enhancement; reduced motion gets the static layout.
const revealCards = document.querySelectorAll('.dish-card, .experience-gallery figure, .review-card');
if (!reducedMotion && 'IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('has-entered');
      revealObserver.unobserve(entry.target);
    });
  }, { threshold: .08 });
  revealCards.forEach(card => { card.classList.add('reveal-ready'); revealObserver.observe(card); });
}
const tableFilm = document.querySelector('#table-film');
new IntersectionObserver(([entry]) => { if (!entry.isIntersecting) tableFilm.pause(); }).observe(tableFilm);
document.addEventListener('visibilitychange', () => { if (document.hidden) tableFilm.pause(); });
