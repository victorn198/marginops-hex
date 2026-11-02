from pathlib import Path
import hashlib, json, subprocess, urllib.request, re

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data'/'source'
RAW.mkdir(parents=True,exist_ok=True)
URL='https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/download/ready-to-use-data/parquet-1m.7z'
archive=RAW/'parquet-1m.7z'
if not archive.exists():
    print('Downloading official SQLBI Contoso 1M dataset...',flush=True)
    with urllib.request.urlopen(URL,timeout=90) as response, (RAW/'download.partial').open('wb') as out:
        while chunk:=response.read(1024*1024): out.write(chunk)
    (RAW/'download.partial').replace(archive)
seven=Path('C:/Program Files/7-Zip/7z.exe')
listing=subprocess.check_output([str(seven),'l','-slt',str(archive)],text=True,encoding='utf-8')
members=listing.split('----------\n')[-1]
for name in re.findall(r'^Path = (.+)$',members,re.M):
    resolved=(RAW/name.strip()).resolve()
    assert resolved.is_relative_to(RAW.resolve()),f'Unsafe archive member: {name}'
target=RAW/'extracted'
if not target.exists():
    target.mkdir()
    subprocess.run([str(seven),'x',str(archive),'-o'+str(target),'-y','-bso0','-bsp0'],check=True)
files=[{'path':str(p.relative_to(ROOT)), 'bytes':p.stat().st_size} for p in target.rglob('*') if p.is_file()]
sha=hashlib.sha256(archive.read_bytes()).hexdigest()
manifest={'source':URL,'source_page':'https://docs.sqlbi.com/contoso-data-generator/','license':'MIT','synthetic':True,'description':'SQLBI Contoso simulated enterprise, published 1M-order scale. Verify actual row count from source tables.','sha256':sha,'files':files}
(RAW/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2),flush=True)
