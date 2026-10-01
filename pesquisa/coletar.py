import json, re, unicodedata, urllib.request, concurrent.futures, hashlib, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT/'pesquisa/fontes/acuolina-dados.json').read_text())
menu = data['data'][0]['menu']
def slug(s):
    return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')
jobs=[]
for sec in menu['sections']:
    for d in sec['dishes']:
        if d.get('picture'):
            jobs.append({'nome':d['name'].strip(),'fonte':'Acuolina','url':'https://acuolina.nyc3.cdn.digitaloceanspaces.com/'+d['picture']+'.jpeg','arquivo':'assets/produtos/'+slug(d['name'])+'-acuolina.jpeg'})
jobs.extend([
 {'nome':'Logo Casa da Esquina','fonte':'Acuolina','url':'https://acuolina.nyc3.cdn.digitaloceanspaces.com/restaurants/62f81cc02373400023678f52/logo_1727651036120.jpeg','arquivo':'assets/logo/casa-da-esquina-acuolina.jpeg'},
 {'nome':'Logo Casa da Esquina','fonte':'PedyUN','url':'https://pedyun.com.br/logos/1712845836757.jpeg','arquivo':'assets/logo/casa-da-esquina-pedyun.jpeg'}])
for nome,arquivo in [
 ('Cheese Burger','101_1757525689218_bd8a37ca.jpg'),('Cheese Bacon','102_1757524952579_5ce1dcbb.jpg'),
 ('Mexicano','103_1757525735645_d75f60bd.jpg'),('Burger da Casa','105_1757525540141_e8d7ba9c.jpg'),
 ('Junior','108_1757525583460_c3b7c73c.jpg'),('Supremo','109_1757525092191_9260abde.jpg'),
 ('Vegetariano','110_1757525634205_31eccf99.jpg'),('Cheddar Crispy','111_1757524891417_7c4a3c72.jpg'),
 ('La Casa Turbo','113_1757525620767_127444aa.jpg'),('Caldo de Carne','81_1757524562740_ab7090da.jpg'),
 ('Caldo de Feijão','83_1757523896729_be6f38aa.jpg'),('Caldo de Frango','82_1757523933476_9273785e.jpg')]:
    jobs.append({'nome':nome,'fonte':'PedyUN','url':'https://files.pedyun.com/yunes-delivery/1712845836757/'+arquivo,'arquivo':'assets/produtos/'+slug(nome)+'-pedyun.jpg'})
def download(job):
    try:
        req=urllib.request.Request(job['url'],headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=40) as r:
            content=r.read(); mime=r.headers.get('Content-Type','')
        if not mime.startswith('image/') or not content.startswith(b'\xff\xd8'): raise ValueError('Resposta não é JPEG')
        (ROOT/job['arquivo']).write_bytes(content)
        return dict(job,status='baixado',bytes=len(content),sha256=hashlib.sha256(content).hexdigest())
    except Exception as exc: return dict(job,status='erro',erro=str(exc))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(download,jobs))
(ROOT/'pesquisa/inventario-imagens.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
lines=['# Inventário das imagens da Casa da Esquina','','Coleta em 30/09/2026. Arquivos preservados como fornecidos pelos canais consultados.','','| Imagem | Canal | Arquivo local | Origem | Status |','|---|---|---|---|---|']
for j in results:lines.append(f"| {j['nome']} | {j['fonte']} | [{Path(j['arquivo']).name}](../{j['arquivo']}) | [Imagem original]({j['url']}) | {j['status']} |")
(ROOT/'pesquisa/INVENTARIO-IMAGENS.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'total':len(results),'baixados':sum(r['status']=='baixado' for r in results),'erros':[r for r in results if r['status']=='erro']},ensure_ascii=False))
