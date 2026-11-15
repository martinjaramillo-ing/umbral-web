import json, pathlib, shutil
root=pathlib.Path(__file__).parent
out=root/'dist'
if out.exists(): shutil.rmtree(out)
out.mkdir()
shutil.copy2(root/'index.html',out/'index.html')
shutil.copytree(root/'static'/'images',out/'images')
data={}
for category in ['libros','encuentros','bitacora','historias','galerias']:
 data[category]=[json.loads(p.read_text(encoding='utf8')) for p in sorted((root/'content'/category).glob('*.json'))]
(out/'content.js').write_text('window.UMBRAL_CONTENT = '+json.dumps(data,ensure_ascii=False)+';\n'+'''(function(){
const data=window.UMBRAL_CONTENT;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const image=(src,alt)=>src?`<img src="${esc(src)}" alt="${esc(alt)}" loading="lazy">`:'';
const tile=(title,sub,body,img)=>`<article class="tile">${image(img,title)}<div class="tile-body"><div class="tag">${esc(sub)}</div><h3>${esc(title)}</h3><p>${esc(body)}</p></div></article>`;
function fill(id,html){const el=document.getElementById(id);if(el&&html)el.innerHTML=html}
fill('libros-lista',data.libros.map(x=>tile(x.titulo,x.autor||x.estado,x.sinopsis,x.portada)).join(''));
fill('encuentros-lista',data.encuentros.sort((a,b)=>a.fecha.localeCompare(b.fecha)).map(x=>`<div class="event" style="margin-bottom:16px"><div class="date"><strong>${esc((x.fecha||'').slice(8,10))}</strong><span>${esc((x.fecha||'').slice(0,7))}</span></div><div><div class="tag">${esc(x.modalidad)} · ${esc(x.hora)}</div><h3>${esc(x.titulo)}</h3><p>${esc(x.descripcion)}</p></div></div>`).join(''));
fill('bitacora-lista',data.bitacora.map(x=>`<article style="margin-top:20px"><strong>${esc(x.titulo)}</strong> · ${esc(x.autor)}<p>${esc(x.resumen)}</p></article>`).join(''));
fill('historias-lista',data.historias.map(x=>tile(x.titulo,x.autor,x.resumen,x.imagen)).join(''));
fill('galeria-lista',data.galerias.map(x=>`<article class="tile">${(x.fotos||[]).slice(0,1).map(f=>image(f,x.titulo)).join('')}<div class="tile-body"><div class="tag">${esc(x.fecha)}</div><h3>${esc(x.titulo)}</h3><p>${esc(x.descripcion)}</p>${(x.fotos||[]).slice(1).map(f=>`<a href="${esc(f)}" target="_blank" rel="noopener">Ver foto</a> `).join('')}</div></article>`).join(''));
})();''',encoding='utf8')
print('Sitio generado en dist/')
