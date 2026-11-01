from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'shell.html').read_text()
for key,file in [('/*THREE_LIB*/','three.min.js'),('/*CLIPPER_LIB*/','clipper.js'),('/*CURVE_DATA*/','curves.json')]:
 s=s.replace(key,(p/file).read_text())
(p/'dist').mkdir(exist_ok=True)
(p/'dist/index.html').write_text(s)
