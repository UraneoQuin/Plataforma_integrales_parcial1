#!/usr/bin/env python3
"""Genera index.html, shared/ y los 14 módulos. Uso: python tools/build.py (desde la raíz)."""
import os, pathlib
R = pathlib.Path(__file__).resolve().parent.parent

MODS = [("riemann","Sumas de Riemann"),("trapecio","Regla del Trapecio"),("punto-medio","Regla del Punto Medio"),
 ("simpson","Regla de Simpson"),("integral-definida","Integral definida y área"),("integracion-directa","Integración directa"),
 ("sustitucion","Sustitución (potencias)"),("exponenciales","Exponenciales"),("logaritmicas","Logarítmicas"),
 ("trigonometricas","Trigonométricas"),("trig-inversas","Trigonométricas inversas"),("hiperbolicas-inversas","Hiperbólicas inversas"),
 ("trinomio","Trinomio ax²+bx+c"),("partes","Integración por partes")]
def phase(i): return 1 if i < 6 else 2 if i < 10 else 3
def folder(i): return f"{i+1:02d}-{MODS[i][0]}"

CSS = """:root{--bg:#fbfaf6;--fg:#1c2433;--mut:#5d6677;--ac:#1d4ed8;--ac2:#b45309;--card:#fff;--bd:#d8d6cc}
@media(prefers-color-scheme:dark){:root{--bg:#111722;--fg:#e7eaf0;--mut:#9ba5b6;--ac:#7aa2ff;--ac2:#f0b35a;--card:#192131;--bd:#2b364a}}
*{box-sizing:border-box}
body{margin:0;font:17px/1.65 Georgia,'Times New Roman',serif;background:var(--bg);color:var(--fg)}
header,main,footer{max-width:960px;margin:auto;padding:1rem}
header{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:.5rem;border-bottom:2px solid var(--fg)}
header a{font:600 1rem system-ui,sans-serif;text-decoration:none;color:var(--fg)}
h1{font-size:clamp(1.8rem,5vw,2.8rem);line-height:1.15;margin:.6rem 0}
h2{margin-top:2rem}
a{color:var(--ac)} a:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid var(--ac2);outline-offset:2px}
.lead{max-width:65ch;color:var(--mut)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:.8rem;margin:1rem 0}
.card{display:block;border:1px solid var(--bd);border-left:5px solid var(--ac);background:var(--card);padding:.7rem .9rem;text-decoration:none;color:var(--fg);font-family:system-ui,sans-serif}
.card.soon{border-left-color:var(--bd);color:var(--mut)}
.card b{display:block}.card small{color:var(--mut)}
.ex,.viz{background:var(--card);border:1px solid var(--bd);padding:1rem;margin:1.2rem 0}
.ex>h3{margin:0 0 .4rem;font-size:1.05rem;color:var(--ac2)}
.ctl{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;font-family:system-ui,sans-serif;font-size:.95rem}
input,select{padding:.3rem .4rem;border:1px solid var(--bd);border-radius:4px;background:var(--bg);color:var(--fg);max-width:100%;font:inherit}
.plot{width:100%;height:360px}.res{font:.9rem ui-monospace,monospace;margin-top:.5rem;overflow-wrap:anywhere}
.katex-display{overflow-x:auto;overflow-y:hidden;padding:.2rem 0}
nav.pn{display:flex;justify-content:space-between;gap:1rem;font-family:system-ui,sans-serif;margin-top:2rem}
.soonmsg{padding:3rem 1rem;text-align:center;border:2px dashed var(--bd);font-size:1.3rem}
footer{color:var(--mut);font:.85rem system-ui,sans-serif}
"""

JS = r"""const Q=(s,r=document)=>r.querySelector(s);
function mk(s){try{const e=s.replace(/(\d)\s*(?=[a-z(])/g,'$1*').replace(/\)\s*(?=[a-z(\d])/g,')*').replace(/\^/g,'**').replace(/\be\b/g,'Math.E').replace(/\bpi\b/g,'Math.PI').replace(/\bln\b/g,'Math.log').replace(/\b(sin|cos|tan|exp|sqrt|abs|atan|asin|acos)\b/g,'Math.$1');return new Function('x','return '+e)}catch(_){return()=>NaN}}
const val=s=>mk(s)(0);
function rule(m,f,a,b,n){const h=(b-a)/n;let s=0;
 if(m=='T'){s=(f(a)+f(b))/2;for(let i=1;i<n;i++)s+=f(a+i*h);return s*h}
 if(m=='S'){s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+i*h);return s*h/3}
 for(let i=0;i<n;i++)s+=f(a+i*h+(m=='R'?h:m=='M'?h/2:0));return s*h}
function shape(m,f,a,b,n){const h=(b-a)/n,X=[],Y=[],P=(x,y)=>{X.push(x);Y.push(y)},N=()=>{X.push(null);Y.push(null)};
 if(m=='S'){for(let i=0;i<n;i+=2){const x0=a+i*h,x1=x0+h,x2=x1+h,y0=f(x0),y1=f(x1),y2=f(x2);P(x0,0);
  for(let k=0;k<=20;k++){const x=x0+k*h/10,t=(x-x1)/h;P(x,y1+t*(y2-y0)/2+t*t*(y0-2*y1+y2)/2)}P(x2,0);N()}return[X,Y]}
 for(let i=0;i<n;i++){const x0=a+i*h,x1=x0+h;let y0,y1;
  if(m=='T'){y0=f(x0);y1=f(x1)}else y0=y1=f(m=='L'?x0:m=='R'?x1:x0+h/2);
  P(x0,0);P(x0,y0);P(x1,y1);P(x1,0);N()}return[X,Y]}
document.querySelectorAll('.viz').forEach(v=>{
 const d=v.dataset,mode=d.mode,area=mode=='area',num=!area&&mode!='direct';
 v.innerHTML=`<div class=ctl>f(x)=<input class=f value="${d.f}" size=14 aria-label="f(x)">`+
  (area?`g(x)=<input class=g value="${d.g||'0'}" size=10 aria-label="g(x)">`:'')+
  `a=<input class=a value="${d.a}" size=5 aria-label="a"> b=<input class=b value="${d.b}" size=5 aria-label="b">`+
  (num?`n=<input type=range class=n min=1 max=100 value=${d.n} aria-label="n"><b class=nv></b>`:'')+
  (mode=='riemann'?`<select class=m aria-label="Tipo de suma"><option value=L>Izquierda<option value=R>Derecha<option value=M>Punto medio</select>`:'')+
  `</div><div class=plot></div><div class=res></div>`;
 const g=s=>Q(s,v);
 function upd(){
  const F=mk(g('.f').value),G=area?mk(g('.g').value):()=>0,a=val(g('.a').value),b=val(g('.b').value);
  const m=mode=='riemann'?g('.m').value:{trap:'T',mid:'M',simpson:'S'}[mode];let n=num?+g('.n').value:0;
  if(m=='S'&&n%2)n++;if(num)g('.nv').textContent=n;
  const xs=Array.from({length:301},(_,i)=>a+(b-a)*i/300),T=[{x:xs,y:xs.map(F),name:'f(x)',mode:'lines',line:{color:'#dc2626'}}];let out;
  if(area){T.push({x:xs,y:xs.map(G),name:'g(x)',mode:'lines',line:{color:'#1d4ed8'},fill:'tonexty',fillcolor:'rgba(29,78,216,.25)'});
   out='Área = '+rule('S',x=>Math.abs(F(x)-G(x)),a,b,4000).toFixed(6)+'  |  Integral con signo de f−g = '+rule('S',x=>F(x)-G(x),a,b,4000).toFixed(6)}
  else if(mode=='direct'){let c=0;const h=(b-a)/300,Fy=xs.map((x,i)=>i?c+=h*(F(x)+F(x-h))/2:0);
   T.push({x:xs,y:Fy,name:'F(x), con F(a)=0',mode:'lines',line:{color:'#1d4ed8'}});out='F(b)−F(a) = '+Fy[300].toFixed(6)+'  (F es una antiderivada de f; las demás difieren en una constante C)'}
  else{const[X,Y]=shape(m,F,a,b,n),ap=rule(m,F,a,b,n),ref=rule('S',F,a,b,2000);
   T.push({x:X,y:Y,name:'aproximación',mode:'lines',fill:'toself',fillcolor:'rgba(29,78,216,.25)',line:{color:'#1d4ed8',width:1}});
   out=`Aproximación (n=${n}) = ${ap.toFixed(6)}  |  Valor de referencia = ${ref.toFixed(6)}  |  Error = ${Math.abs(ref-ap).toExponential(2)}`}
  g('.res').textContent=out;
  Plotly.react(g('.plot'),T,{margin:{t:10,l:40,r:10,b:30},paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{color:getComputedStyle(document.body).color},legend:{orientation:'h'}},{responsive:true})}
 v.addEventListener('input',upd);upd()});
"""

def viz(mode, f, a, b, n=4, g=""):
    return f'<div class="viz" data-mode="{mode}" data-f="{f}" data-g="{g}" data-a="{a}" data-b="{b}" data-n="{n}"></div>'
def ex(t, body): return f'<div class="ex"><h3>{t}</h3>{body}</div>'

C = {}
C[0] = (r"""<p>Dividimos $[a,b]$ en $n$ subintervalos de ancho $\Delta x=\frac{b-a}{n}$ y sumamos áreas de rectángulos:</p>
$$L_n=\sum_{i=0}^{n-1}f(x_i)\Delta x,\qquad R_n=\sum_{i=1}^{n}f(x_i)\Delta x,\qquad M_n=\sum_{i=1}^{n}f(\bar x_i)\Delta x,\ \ \bar x_i=\tfrac{x_{i-1}+x_i}{2}$$
<p>Al aumentar $n$, las tres sumas convergen a $\int_a^b f(x)\,dx$.</p>""",
 viz("riemann","x^2",0,2,4),
 ex("Ejemplo 1: $f(x)=x^2$ en $[0,2]$, $n=4$", r"""<p>$\Delta x=0.5$; nodos $0,\,0.5,\,1,\,1.5,\,2$ con $f=0,\,0.25,\,1,\,2.25,\,4$.</p>
$$L_4=0.5(0+0.25+1+2.25)=1.75,\qquad R_4=0.5(0.25+1+2.25+4)=3.75$$
<p>Puntos medios $0.25,\,0.75,\,1.25,\,1.75$: $M_4=0.5(0.0625+0.5625+1.5625+3.0625)=2.625$.</p>
<p>Valor exacto: $\int_0^2x^2dx=\tfrac83\approx2.6667$. $L_4$ subestima, $R_4$ sobreestima y $M_4$ es la más cercana.</p>""")+
 ex(r"Ejemplo 2: $\int_1^3\frac1x\,dx$ con $n=5$", r"""<p>$\Delta x=0.4$; nodos $1,\,1.4,\,1.8,\,2.2,\,2.6,\,3$.</p>
$$L_5=0.4(1+0.7143+0.5556+0.4545+0.3846)\approx1.2436$$
$$R_5=0.4(0.7143+0.5556+0.4545+0.3846+0.3333)\approx0.9769$$
<p>Puntos medios $1.2,\,1.6,\,2,\,2.4,\,2.8$: $M_5=0.4(0.8333+0.625+0.5+0.4167+0.3571)\approx1.0929$. Exacto: $\ln3\approx1.0986$.</p>"""))

C[1] = (r"""<p>Se reemplaza cada rectángulo por un trapecio que une los puntos $(x_{i-1},f(x_{i-1}))$ y $(x_i,f(x_i))$. El área de cada trapecio es $\frac{\Delta x}{2}\,[f(x_{i-1})+f(x_i)]$; al sumar, los nodos interiores aparecen dos veces:</p>
$$T_n=\frac{\Delta x}{2}\Big[f(x_0)+2\sum_{i=1}^{n-1}f(x_i)+f(x_n)\Big],\qquad \Delta x=\frac{b-a}{n}$$""",
 viz("trap","x^2",0,2,4),
 ex("Ejemplo 1: $\int_0^2x^2dx$, $n=4$", r"""<p>$\Delta x=0.5$, $f(x_i)=0,\,0.25,\,1,\,2.25,\,4$.</p>
$$T_4=\frac{0.5}{2}\big[0+2(0.25+1+2.25)+4\big]=0.25\cdot11=2.75$$
<p>Exacto $2.6667$; error $\approx0.0833$ (sobreestima porque $x^2$ es convexa).</p>""")+
 ex(r"Ejemplo 2: $\int_0^{\pi/2}\sin x\,dx$, $n=4$", r"""<p>$\Delta x=\pi/8$; $\sin x_i=0,\,0.3827,\,0.7071,\,0.9239,\,1$.</p>
$$T_4=\frac{\pi}{16}\big[0+2(0.3827+0.7071+0.9239)+1\big]=\frac{\pi}{16}(5.0273)\approx0.9871$$
<p>Exacto $1$; error $\approx0.0129$ (subestima porque $\sin x$ es cóncava).</p>"""))

C[2] = (r"""<p>En cada subintervalo se evalúa $f$ en su punto medio y se forma un rectángulo:</p>
$$M_n=\Delta x\sum_{i=1}^{n}f(\bar x_i),\qquad \bar x_i=\frac{x_{i-1}+x_i}{2},\quad \Delta x=\frac{b-a}{n}$$
<p>Suele ser más precisa que el trapecio: el error de $M_n$ es aproximadamente la mitad del de $T_n$ y de signo contrario.</p>""",
 viz("mid","x^2",0,2,4),
 ex("Ejemplo 1: $\int_0^2x^2dx$, $n=4$", r"""<p>Puntos medios $0.25,\,0.75,\,1.25,\,1.75$ con $f=0.0625,\,0.5625,\,1.5625,\,3.0625$.</p>
$$M_4=0.5\,(5.25)=2.625\quad(\text{exacto }2.6667)$$""")+
 ex(r"Ejemplo 2: $\int_0^{\pi/2}\cos x\,dx$, $n=4$", r"""<p>$\Delta x=\pi/8$; puntos medios $\pi/16,\,3\pi/16,\,5\pi/16,\,7\pi/16$.</p>
$$M_4=\frac{\pi}{8}(0.9808+0.8315+0.5556+0.1951)=\frac{\pi}{8}(2.5629)\approx1.0065$$
<p>Exacto $1$; error $\approx0.0065$.</p>"""))

C[3] = (r"""<p>Aproxima $f$ con parábolas que pasan por tres nodos consecutivos. Por eso <b>$n$ debe ser par</b>: se agrupan los subintervalos de dos en dos.</p>
$$S_n=\frac{\Delta x}{3}\Big[f(x_0)+4\!\!\sum_{i\ \text{impar}}\!\!f(x_i)+2\!\!\sum_{i\ \text{par}}\!\!f(x_i)+f(x_n)\Big]$$
<p>Es exacta para polinomios de grado $\le3$.</p>""",
 viz("simpson","sin(x)",0,"pi",4),
 ex("Ejemplo 1: $\int_0^2x^2dx$, $n=4$", r"""$$S_4=\frac{0.5}{3}\big[0+4(0.25)+2(1)+4(2.25)+4\big]=\frac{16}{6}=\frac83$$
<p>Coincide con el valor exacto, porque $x^2$ tiene grado $\le3$.</p>""")+
 ex(r"Ejemplo 2: $\int_0^{\pi}\sin x\,dx$, $n=4$", r"""<p>$\Delta x=\pi/4$; $\sin x_i=0,\,0.7071,\,1,\,0.7071,\,0$.</p>
$$S_4=\frac{\pi}{12}\big[0+4(0.7071)+2(1)+4(0.7071)+0\big]=\frac{\pi}{12}(7.6569)\approx2.0046$$
<p>Exacto $2$; error $\approx0.0046$.</p>"""))

C[4] = (r"""<p><b>Teorema Fundamental del Cálculo:</b> si $F'=f$ en $[a,b]$, entonces</p>
$$\int_a^b f(x)\,dx=F(b)-F(a)$$
<p>El <b>área</b> no es la integral con signo: $\text{Área}=\int_a^b|f(x)|\,dx$. Entre dos curvas: $\int_a^b|f(x)-g(x)|\,dx$. Cambie $f$, $g$, $a$ y $b$ en el visualizador (ej.: $f=2x$, $g=x^2$).</p>""",
 viz("area","2x",0,2,0,"x^2"),
 ex(r"Ejemplo 1: $\int_0^2(3x^2-2x+1)\,dx$", r"""$$F(x)=x^3-x^2+x\ \Rightarrow\ F(2)-F(0)=(8-4+2)-0=6$$""")+
 ex("Ejemplo 2: área entre $f(x)=2x$ y $g(x)=x^2$", r"""<p>Intersecciones: $x^2=2x\Rightarrow x=0,\ x=2$. En $(0,2)$, $2x\ge x^2$.</p>
$$A=\int_0^2(2x-x^2)\,dx=\Big[x^2-\tfrac{x^3}{3}\Big]_0^2=4-\tfrac83=\tfrac43$$"""))

C[5] = (r"""<p>Fórmulas básicas, más linealidad: $\int[\alpha f+\beta g]=\alpha\!\int f+\beta\!\int g$.</p>
$$\int x^n\,dx=\frac{x^{n+1}}{n+1}+C\ (n\neq-1),\qquad \int\frac{dx}{x}=\ln|x|+C$$
<p>El visualizador dibuja $f$ y una antiderivada $F$ calculada numéricamente con $F(a)=0$. Pruebe $f=x^2-1$: $F$ es $\frac{x^3}{3}-x$.</p>""",
 viz("direct","x^2-1",0,3,0),
 ex(r"Ejemplo 1: $\int(x-1)(x+1)\,dx$", r"""$$\int(x^2-1)\,dx=\frac{x^3}{3}-x+C$$""")+
 ex(r"Ejemplo 2: $\int\Big(\frac{3}{x^2}-\frac{9}{\sqrt x}\Big)dx$", r"""$$3\!\int x^{-2}dx-9\!\int x^{-1/2}dx=3\cdot\frac{x^{-1}}{-1}-9\cdot\frac{x^{1/2}}{1/2}+C=-\frac3x-18\sqrt x+C$$""")+
 ex(r"Ejemplo 3: $\int\Big(x-1-\frac1x\Big)dx$", r"""$$\frac{x^2}{2}-x-\ln|x|+C$$
<p>Verificación por derivación: $\frac{d}{dx}\big[\frac{x^2}{2}-x-\ln|x|\big]=x-1-\frac1x$ ✓</p>"""))

HEAD = """<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s · Cálculo Integral UTP</title><link rel="stylesheet" href="%sshared/style.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]})"></script>
<script defer src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script><script defer src="%sshared/app.js"></script></head><body>
<header><a href="%sindex.html">Cálculo Integral · UTP</a><span>Tecnología en Desarrollo de Software · 2026-II</span></header><main>"""
FOOT = "</main><footer>Universidad Tecnológica de Pereira · Departamento de Matemáticas. Proyecto colaborativo, Fase 1.</footer></body></html>"

def write(p, s):
    p = R / p; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding="utf-8")

write("shared/style.css", CSS); write("shared/app.js", JS)

cards = ""
for i, (_, t) in enumerate(MODS):
    soon = i >= 6
    cards += f'<a class="card{" soon" if soon else ""}" href="modules/{folder(i)}/index.html"><b>{i+1}. {t}</b><small>{"Próximamente - Fase %d" % phase(i) if soon else "Disponible · Fase 1"}</small></a>'
write("index.html", HEAD % ("Inicio", "", "", "") + f"""<h1>Cálculo integral, visto y comprobado</h1>
<p class="lead">Aproxime áreas con rectángulos, trapecios y parábolas, mueva los límites de una integral y compare cada resultado con el valor de referencia. Elija un módulo.</p>
<div class="grid">{cards}</div>""" + FOOT)

for i, (_, t) in enumerate(MODS):
    d = f"modules/{folder(i)}/index.html"
    if i < 6:
        theory, v, exs = C[i]; body = f"<h1>{i+1}. {t}</h1><h2>Teoría</h2>{theory}<h2>Visualizador interactivo</h2>{v}<h2>Ejemplos resueltos</h2>{exs}"
    else:
        body = f'<h1>{i+1}. {t}</h1><div class="soonmsg">Próximamente - Fase {phase(i)}</div>'
    prev = f'<a href="../{folder(i-1)}/index.html">← {MODS[i-1][1]}</a>' if i else "<span></span>"
    nxt = f'<a href="../{folder(i+1)}/index.html">{MODS[i+1][1]} →</a>' if i < 13 else "<span></span>"
    write(d, HEAD % (t, "../../", "../../", "../../") + body + f'<nav class="pn">{prev}{nxt}</nav>' + FOOT)
print("Sitio generado en", R)
