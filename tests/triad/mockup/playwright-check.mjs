// ALT-TRIAD-001 — pruebas de navegador sobre la maqueta aislada (sin red, sin datos reales).
// Uso: node tests/triad/mockup/playwright-check.mjs   (usa el Playwright local ya instalado; no instala nada)
// Escribe tests/triad/mockup/playwright-result.json. Sale con 1 si algun control falla.
import {createRequire} from 'node:module';
import {pathToFileURL, fileURLToPath} from 'node:url';
import {writeFileSync} from 'node:fs';
import {dirname, join} from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const toolRoot = process.env.ALTIORA_PLAYWRIGHT_ROOT || join(process.env.USERPROFILE || process.env.HOME, '.altiora-tools', 'mcp-browser');
const {chromium} = createRequire(join(toolRoot, 'package.json'))('playwright');
const url = pathToFileURL(join(here, 'index.html')).href;
const results = [];
const check = (id, ok, detail) => { results.push({id, status: ok ? 'PASS' : 'FAIL', detail}); };

const browser = await chromium.launch({channel: process.env.ALTIORA_BROWSER_CHANNEL || 'chrome'}); // Chrome del sistema: no descarga navegadores
try {
  // --- 360x640 con JS ---
  const ctx = await browser.newContext({viewport: {width: 360, height: 640}, deviceScaleFactor: 1});
  const page = await ctx.newPage();
  await page.goto(url);
  await page.evaluate(() => document.fonts.ready);

  const cta = await page.locator('#cta-principal').boundingBox();
  const scrollY = await page.evaluate(() => window.scrollY);
  check('M1-cta-visible-sin-scroll-360x640', cta && cta.y >= 0 && cta.y + cta.height <= 640 && scrollY === 0,
    `CTA y=${cta?.y.toFixed(1)} alto=${cta?.height.toFixed(1)} borde inferior=${(cta.y + cta.height).toFixed(1)} de 640; scrollY=${scrollY}`);

  const ov = await page.evaluate(() => {
    const de = document.documentElement; const w = de.clientWidth;
    const wide = [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > w + 0.5).map(e => e.tagName + (e.id ? '#' + e.id : ''));
    return {scrollWidth: de.scrollWidth, clientWidth: w, wide};
  });
  check('M2-sin-desbordamiento-horizontal', ov.scrollWidth <= ov.clientWidth && ov.wide.length === 0, JSON.stringify(ov));

  // --- Nombres accesibles (WCAG 2.5.3) ---
  const names = await page.$$eval('.btn-card-select', as => as.map(a => ({visible: a.textContent.trim(), aria: a.getAttribute('aria-label')})));
  check('A1-label-in-name', names.length === 3 && names.every(n => n.aria.startsWith(n.visible)), JSON.stringify(names));
  const byRole = await page.getByRole('link', {name: /^Elegir esta planta/}).count();
  check('A2-nombre-accesible-por-rol', byRole === 3, `enlaces con nombre accesible que empieza por el texto visible: ${byRole}`);

  // --- Teclado ---
  await page.keyboard.press('Tab');
  const first = await page.evaluate(() => document.activeElement.id);
  const ring = await page.evaluate(() => { const s = getComputedStyle(document.activeElement); return {w: s.outlineWidth, style: s.outlineStyle, color: s.outlineColor}; });
  check('K1-primer-tab-es-CTA-con-foco-visible', first === 'cta-principal' && ring.w === '3px' && ring.style === 'solid', JSON.stringify({first, ring}));
  const order = [];
  for (let i = 0; i < 30; i++) { await page.keyboard.press('Tab'); const cur = await page.evaluate(() => { const e = document.activeElement; return e.id || e.className || e.tagName; }); order.push(cur); if (cur === 'btn-cta-submit') break; } // una sola vuelta, hasta el boton de envio
  const reachesAll = ['campo-planta', 'campo-nombre', 'campo-direccion', 'campo-telefono', 'campo-notas'].every(id => order.includes(id)) && order.filter(x => x === 'btn-card-select').length === 3;
  check('K2-todos-los-controles-alcanzables-por-teclado', reachesAll, order.join(' > '));
  await page.reload();
  await page.focus('a[data-planta="sansevieria"]');
  await page.keyboard.press('Enter');
  const kb = await page.evaluate(() => ({val: document.getElementById('campo-planta').value, focus: document.activeElement.id}));
  check('K3-enter-en-ficha-preselecciona-y-mueve-foco', kb.val === 'sansevieria' && kb.focus === 'campo-planta', JSON.stringify(kb));

  // --- Preseleccion por URL (enlace compartible) ---
  const p2 = await ctx.newPage();
  await p2.goto(url + '?planta=ficus#pedido');
  check('P1-url-con-query-preselecciona', (await p2.inputValue('#campo-planta')) === 'ficus', 'valor del select tras cargar ?planta=ficus#pedido');
  await p2.goto(url + '?planta=NOEXISTE#pedido');
  check('P2-valor-invalido-se-ignora', (await p2.inputValue('#campo-planta')) === '', 'select queda vacio');
  await p2.close();

  // --- Formulario en modo prueba ---
  await page.goto(url);
  await page.click('button.btn-cta-submit');
  const errs = await page.$$eval('.error-text', e => e.map(x => x.textContent));
  const inv = await page.$$eval('[aria-invalid="true"]', e => e.length);
  const firstFocus = await page.evaluate(() => document.activeElement.id);
  check('F1-envio-vacio-muestra-errores-accesibles', errs.length === 4 && inv === 4 && firstFocus === 'campo-planta', JSON.stringify({errs: errs.length, invalid: inv, firstFocus}));
  await page.selectOption('#campo-planta', 'monstera');
  await page.fill('#campo-nombre', 'Persona de Prueba');
  await page.fill('#campo-direccion', 'Calle Ficticia 123');
  await page.fill('#campo-telefono', '+000 000 0000');
  await page.click('button.btn-cta-submit');
  const res = await page.locator('#resultado').innerText();
  check('F2-envio-valido-confirma-sin-red', /Pedido de prueba registrado/.test(res) && (await page.locator('.error-text').count()) === 0, res);

  // --- Contraste sobre colores renderizados (incluye hover y opacidades) ---
  const contrast = await page.evaluate(() => {
    const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
    const parse = s => (s.match(/[\d.]+/g) || []).map(Number);
    const L = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
    const ratio = (a, b) => { const x = L(a), y = L(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
    const bgOf = el => { for (let e = el; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c.length >= 3 && (c[3] === undefined || c[3] > 0)) return c.slice(0, 3); } return [255, 255, 255]; };
    const pair = (name, el, fgOverride, bgOverride) => {
      const s = getComputedStyle(el); const fg = fgOverride || parse(s.color).slice(0, 3); const bg = bgOverride || bgOf(el);
      const op = parseFloat(s.opacity);
      return {name, fg: fg.join(','), bg: bg.join(','), opacity: op, ratio: +ratio(fg, bg).toFixed(2)};
    };
    const out = [];
    out.push(pair('CTA reposo', document.querySelector('#cta-principal')));
    out.push(pair('texto cuerpo sobre canvas', document.querySelector('.hero-subtext')));
    out.push(pair('hero-trust (muted)', document.querySelector('.hero-trust')));
    out.push(pair('btn-card-select reposo', document.querySelector('.btn-card-select')));
    out.push(pair('badge-tag', document.querySelector('.badge-tag')));
    out.push(pair('FAQ summary', document.querySelector('.faq-item summary')));
    out.push(pair('FAQ respuesta', document.querySelector('.faq-answer p')));
    // placeholder: color real fijado en CSS (#5B6B5F) sobre #FFFFFF
    out.push(pair('placeholder', document.querySelector('#campo-nombre'), [0x5B, 0x6B, 0x5F], [255, 255, 255]));
    out.push(pair('error-text', (() => { const s = document.createElement('span'); s.className = 'error-text'; document.body.append(s); return s; })(), null, [255, 255, 255]));
    return out;
  });
  // estados hover: se miden con el raton encima
  await page.setViewportSize({width: 1280, height: 800});
  await page.goto(url);
  const hoverPairs = [];
  for (const [name, sel, bgExpected] of [['CTA hover', '#cta-principal'], ['btn-card-select hover', '.btn-card-select']]) {
    await page.hover(sel); await page.waitForTimeout(250);
    hoverPairs.push(await page.evaluate(([n, s]) => {
      const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
      const parse = x => (x.match(/[\d.]+/g) || []).map(Number).slice(0, 3);
      const L = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
      const st = getComputedStyle(document.querySelector(s)); const fg = parse(st.color), bg = parse(st.backgroundColor);
      const a = L(fg), b = L(bg);
      return {name: n, fg: fg.join(','), bg: bg.join(','), ratio: +((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)).toFixed(2)};
    }, [name, sel]));
  }
  const all = [...contrast, ...hoverPairs];
  const failing = all.filter(p => p.ratio < 4.5);
  check('C1-contraste-renderizado-texto-ge-4.5', failing.length === 0, JSON.stringify({failing, total: all.length}));
  results.push({id: 'C-detalle', status: 'INFO', detail: all});

  // --- Sin JS (resiliencia) ---
  const nojs = await browser.newContext({viewport: {width: 360, height: 640}, javaScriptEnabled: false});
  const pn = await nojs.newPage(); await pn.goto(url);
  const ctaN = await pn.locator('#cta-principal').boundingBox();
  const href = await pn.getAttribute('a[data-planta="monstera"]', 'href');
  check('R1-sin-JS-CTA-visible-y-enlaces-validos', ctaN.y + ctaN.height <= 640 && href === '?planta=monstera#pedido', `CTA borde inferior=${(ctaN.y + ctaN.height).toFixed(1)}; href=${href}; sin JS la preseleccion no ocurre y se elige en el select (degradacion esperada)`);

  let posted = false; pn.on('request', r => { if (r.method() === 'POST') posted = true; });
  await pn.click('button.btn-cta-submit'); await pn.waitForTimeout(300);
  check('R3-sin-JS-envio-vacio-bloqueado-por-validacion-nativa', !posted && pn.url().startsWith('file:') && !pn.url().includes('api/pedido'), `POST emitido=${posted}; url=${pn.url().slice(-40)}`);

  // --- Movimiento reducido ---
  const rm = await browser.newContext({viewport: {width: 1280, height: 800}, reducedMotion: 'reduce'});
  const pr = await rm.newPage(); await pr.goto(url); await pr.hover('#cta-principal'); await pr.waitForTimeout(100);
  const tf = await pr.evaluate(() => getComputedStyle(document.querySelector('#cta-principal')).transform);
  check('R2-reduced-motion-sin-transform-en-hover', tf === 'none', `transform=${tf}`);
} finally {
  await browser.close();
}
const failed = results.filter(r => r.status === 'FAIL');
const out = {run_at: new Date().toISOString(), target: 'tests/triad/mockup/index.html', summary: {pass: results.filter(r => r.status === 'PASS').length, fail: failed.length}, results};
writeFileSync(join(here, 'playwright-result.json'), JSON.stringify(out, null, 2));
for (const r of results.filter(r => r.status !== 'INFO')) console.log(r.status.padEnd(4), r.id, '-', typeof r.detail === 'string' ? r.detail.slice(0, 200) : '');
console.log(`\n${out.summary.pass} PASS / ${out.summary.fail} FAIL`);
process.exit(failed.length ? 1 : 0);
