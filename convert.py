import argparse, os, tempfile, zipfile, shutil, sys
from pathlib import Path
from leveldb import LevelDB
from palette import patch

ALIASES=(b'minecraft:sea_lantern',b'minecraft:seaLantern',b'minecraft:sealantern')
def main():
 p=argparse.ArgumentParser(description='Convert a copy of a Bedrock .mcworld archive')
 p.add_argument('input',type=Path);p.add_argument('output',type=Path);p.add_argument('--scan',action='store_true',help='Report without writing an output world')
 a=p.parse_args(); src=a.input.resolve(); dst=a.output.resolve()
 if src==dst or dst.exists():p.error('Output must be a new file distinct from input')
 with tempfile.TemporaryDirectory(prefix='railfix_') as tmp:
  root=Path(tmp)/'world';root.mkdir()
  with zipfile.ZipFile(src,metadata_encoding='utf-8') as z:
   for item in z.infolist():
    name=item.filename.replace('\\','/')
    if name.startswith('/') or '..' in name.split('/') or ':' in name:raise ValueError('Unsafe archive path: '+name)
   z.extractall(root)
  if not (root/'level.dat').is_file() or not (root/'db').is_dir():raise ValueError('Not a Bedrock world archive')
  db=LevelDB(str(root/'db')); edits=[];count=0; legacy=0
  try:
   for k,v in db.iterate():
    if len(k) in (10,14) and k[-2]==47:
     if v and v[0] in (0,2,3,4,5,6,7):legacy+=v[1:4097].count(bytes([169]))
     if any(alias in v for alias in ALIASES):
      new,n,entries=patch(v)
      if entries:edits.append((k,new));count+=n
    elif len(k) in (9,13) and k[-1]==48:legacy+=v[:32768].count(bytes([169]))
   print(f'Found {count} lantern blocks in {len(edits)} subchunks; legacy numeric blocks: {legacy}.')
   if legacy:raise ValueError('Legacy numeric sea lanterns detected; conversion unsupported. No output created.')
   if a.scan:return
   for k,v in edits:db.put(k,v)
   for k,v in edits:
    if db.get(k)!=v:raise ValueError('Database write verification failed')
  finally:db.close()
  dst.parent.mkdir(parents=True,exist_ok=True)
  tempout=dst.with_name(dst.name+'.partial')
  if tempout.exists():raise FileExistsError(tempout)
  try:
   with zipfile.ZipFile(tempout,'x',zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as z:
    for base,dirs,files in os.walk(root):
     for f in files:
      path=Path(base)/f
      if path.parent.name=='db' and f in ('LOCK','LOG','LOG.old'):continue
      z.write(path,path.relative_to(root).as_posix())
   with zipfile.ZipFile(tempout) as z:
    bad=z.testzip()
    if bad:raise ValueError('Output integrity check failed: '+bad)
   os.rename(tempout,dst)
  finally:
   if tempout.exists():tempout.unlink()
  print('Created:',dst)
if __name__=='__main__':
 try:main()
 except Exception as exc: print('Error:',exc,file=sys.stderr);sys.exit(1)
