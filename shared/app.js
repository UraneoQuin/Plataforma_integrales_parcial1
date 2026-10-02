const Q=(s,r=document)=>r.querySelector(s);
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
