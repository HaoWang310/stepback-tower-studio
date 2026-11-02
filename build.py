from pathlib import Path
import gzip,base64
p=Path(__file__).resolve().parent
s=(p/'shell.html').read_text()
for key,file in [('/*THREE_LIB*/','three.min.js'),('/*CURVE_DATA*/','curves.json')]:
 s=s.replace(key,(p/file).read_text())
packed=base64.b64encode(gzip.compress((p/'clipper.js').read_bytes(),9,mtime=0)).decode()
s=s.replace('/*CLIPPER_LIB*/',"window.clipperReady=(async()=>{const b=Uint8Array.from(atob('"+packed+"'),c=>c.charCodeAt(0));const s=await new Response(new Blob([b]).stream().pipeThrough(new DecompressionStream('gzip'))).text();(0,eval)(s)})();")
s=s.replace('/*CLIMATE_MODULE*/',(p/'climate.js').read_text().replace('/*WEATHER_DATA*/',(p/'weather.json').read_text()))
(p/'dist').mkdir(exist_ok=True)
(p/'dist/index.html').write_text(s)
