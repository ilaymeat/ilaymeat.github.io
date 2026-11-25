// מרנדר שכבות טקסט שקופות (PNG) בגודל הסרטון מתוך plan.json, בסגנון ILAY MEAT.
// עברית ומספרים מוצגים נכון מימין לשמאל, כי הדפדפן עושה את הסידור.
// שימוש: node render_overlays.js <plan.json> <תיקיית פלט>
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const [planPath, outDir] = process.argv.slice(2);
if (!planPath || !outDir) { console.error('usage: node render_overlays.js plan.json outDir'); process.exit(2); }
const plan = JSON.parse(fs.readFileSync(planPath, 'utf8'));
const W = plan.width || 1080, H = plan.height || 1920;
const fontDir = path.join(__dirname, '..', 'fonts');
const font = f => 'data:font/' + (f.endsWith('woff2') ? 'woff2' : 'woff') + ';base64,' + fs.readFileSync(path.join(fontDir, f)).toString('base64');

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
// מספרים ואנגלית בתוך bdi כדי שלא יקפצו לצד הלא נכון
const bidi = s => esc(s).replace(/([0-9A-Za-z][0-9A-Za-z₪\-–.,:&' ]*[0-9A-Za-z₪]|[0-9A-Za-z])/g, '<bdi dir="ltr">$1</bdi>');
const mark = s => bidi(s).replace(/\*([^*]+)\*/g, '<span class="hl">$1</span>');

const css = `
@font-face{font-family:Secular;src:url(${font('secular-one-400-hebrew.woff2')}) format('woff2');unicode-range:U+0590-05FF,U+FB1D-FB4F}
@font-face{font-family:Secular;src:url(${font('secular-one-400-latin.woff')}) format('woff')}
@font-face{font-family:Heebo;font-weight:100 900;src:url(${font('heebo-100-900-hebrew.woff')}) format('woff');unicode-range:U+0590-05FF,U+FB1D-FB4F}
@font-face{font-family:Heebo;font-weight:100 900;src:url(${font('heebo-100-900-latin.woff')}) format('woff')}
:root{--coal:#14100e;--cream:#f6ede4;--gold:#d6a656;--ember:#c8402a;--wa:#1fae5b}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px;background:transparent;direction:rtl;font-family:Heebo,sans-serif;color:var(--cream)}
.stage{position:absolute;inset:0}
.shade-top{position:absolute;left:0;right:0;top:0;height:46%;background:linear-gradient(180deg,rgba(20,16,14,.78),rgba(20,16,14,0))}
.shade-bot{position:absolute;left:0;right:0;bottom:0;height:46%;background:linear-gradient(0deg,rgba(20,16,14,.82),rgba(20,16,14,0))}
.box{position:absolute;left:72px;right:72px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:18px}
.top{top:250px}.bottom{bottom:330px}
.kicker{font-family:Heebo;font-weight:800;font-size:40px;letter-spacing:.02em;color:var(--gold);display:flex;align-items:center;gap:18px}
.kicker::before,.kicker::after{content:"";width:46px;height:4px;border-radius:2px;background:var(--ember)}
.text{font-family:Secular;font-size:92px;line-height:1.08;text-wrap:balance;text-shadow:0 4px 24px rgba(0,0,0,.55)}
.hook .text{font-size:120px}
.hl{color:var(--gold);background:linear-gradient(transparent 72%,rgba(200,64,42,.85) 72%,rgba(200,64,42,.85) 92%,transparent 92%);padding:0 .08em}
.end{position:absolute;left:0;right:0;top:40%;bottom:0;background:linear-gradient(180deg,rgba(20,16,14,0) 0%,rgba(20,16,14,.93) 16%,var(--coal) 100%);display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding-top:190px;gap:30px;text-align:center}
.brand{font-family:Secular;font-size:120px;color:var(--gold);direction:ltr;letter-spacing:.02em}
.sub{font-family:Secular;font-size:64px}
.price{display:inline-flex;align-items:baseline;gap:20px;border:3px solid var(--gold);border-radius:999px;padding:14px 46px;font-family:Heebo;font-weight:700;font-size:46px}
.price b{font-family:Secular;font-weight:400;font-size:84px;color:var(--gold)}
.cta{display:inline-flex;align-items:center;gap:20px;background:var(--wa);color:#fff;border-radius:999px;padding:22px 54px;font-family:Heebo;font-weight:800;font-size:52px;box-shadow:0 14px 40px rgba(0,0,0,.45)}
.phone{font-family:Heebo;font-weight:700;font-size:46px;color:var(--cream);opacity:.9}
`;

function body(o) {
  if (o.type === 'end') {
    return `<div class="end">
      <div class="brand">${esc(o.brand || 'ILAY MEAT')}</div>
      ${o.sub ? `<div class="sub">${mark(o.sub)}</div>` : ''}
      ${o.price ? `<div class="price"><span>${esc(o.priceLabel || '')}</span><b>${bidi(o.price)}</b><span>${esc(o.priceUnit || '')}</span></div>` : ''}
      ${o.cta ? `<div class="cta">${mark(o.cta)}</div>` : ''}
      ${o.phone ? `<div class="phone"><bdi dir="ltr">${esc(o.phone)}</bdi></div>` : ''}
    </div>`;
  }
  const where = o.pos === 'bottom' ? 'bottom' : 'top';
  return `<div class="shade-${where === 'top' ? 'top' : 'bot'}"></div>
    <div class="box ${where} ${o.type === 'hook' ? 'hook' : ''}">
      ${o.kicker ? `<div class="kicker">${mark(o.kicker)}</div>` : ''}
      <div class="text">${(o.lines || [o.text]).map(mark).join('<br>')}</div>
    </div>`;
}

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  for (const [i, o] of plan.overlays.entries()) {
    await page.setContent(`<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>${css}</style></head><body><div class="stage">${body(o)}</div></body></html>`);
    await page.evaluate(() => document.fonts.ready);
    const file = path.join(outDir, `ov${String(i + 1).padStart(2, '0')}.png`);
    await page.screenshot({ path: file, omitBackground: true });
    console.log(file);
  }
  await browser.close();
})();
