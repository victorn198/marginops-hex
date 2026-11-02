from pathlib import Path
import hashlib, json, urllib.request
import duckdb

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'data'/'source'/'extracted'
target=ROOT/'data'/'published'
target.mkdir(parents=True,exist_ok=True)
con=duckdb.connect()
manifest={'dataset':'SQLBI Contoso 1M','synthetic':True,'license':'MIT','source':'https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/tag/ready-to-use-data','source_archive_sha256':json.loads((ROOT/'data'/'source'/'manifest.json').read_text())['sha256'],'tables':{}}
for file in source.glob('*.parquet'):
    path=file.as_posix()
    projection='CustomerKey, GeoAreaKey, StartDT, EndDT, Continent, City, StateFull, Country, CountryFull' if file.stem=='customer' else '*'
    output=(target/file.name).as_posix()
    con.execute(f"COPY (SELECT {projection} FROM read_parquet('{path}')) TO '{output}' (FORMAT PARQUET, COMPRESSION ZSTD)")
    manifest['tables'][file.stem]={'file':file.name,'rows':con.execute('SELECT count(*) FROM read_parquet(?)',[output]).fetchone()[0],'bytes':Path(output).stat().st_size,'sha256':hashlib.sha256(Path(output).read_bytes()).hexdigest(),'columns':[x[0] for x in con.execute('DESCRIBE SELECT * FROM read_parquet(?)',[output]).fetchall()]}
sales=(target/'sales.parquet').as_posix()
row=con.execute('SELECT min(OrderDate)::DATE,max(OrderDate)::DATE,count(DISTINCT OrderKey),count(DISTINCT CustomerKey) FROM read_parquet(?)',[sales]).fetchone()
manifest['coverage']={'start':str(row[0]),'end':str(row[1]),'orders':row[2],'active_customer_keys':row[3]}
manifest['customer_projection']='Unneeded identity and address-like columns removed, although upstream customers are fictional.'
(target/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
license_url='https://raw.githubusercontent.com/sql-bi/Contoso-Data-Generator-V2-Data/main/LICENSE'
(ROOT/'DATA_LICENSE').write_bytes(urllib.request.urlopen(license_url,timeout=30).read())
print(json.dumps({'coverage':manifest['coverage'],'sales_rows':manifest['tables']['sales']['rows'],'tables':len(manifest['tables']),'public_bytes':sum(t['bytes'] for t in manifest['tables'].values())}))
