import struct, warnings
from amulet_nbt import load_many, ReadContext, NamedTag, CompoundTag, StringTag, IntTag
warnings.filterwarnings('ignore',category=DeprecationWarning)
NAMES={'minecraft:sea_lantern','minecraft:seaLantern','minecraft:sealantern'}; TARGET='railfix:conductive_sea_lantern'
replacement=NamedTag(CompoundTag({'name':StringTag(TARGET),'states':CompoundTag({}),'version':IntTag(18168865)})).save_to(compressed=False,little_endian=True)
def patch(v):
 if not v or v[0] not in (1,8,9): raise ValueError('unsupported subchunk version')
 count=1 if v[0]==1 else v[1]
 pos={1:1,8:2,9:3}[v[0]]; replacements=[]; block_count=0
 for layer in range(count):
  h=v[pos]; pos+=1; bits=h>>1
  if h&1 or bits not in (0,1,2,3,4,5,6,8,16): raise ValueError('unsupported palette encoding')
  if bits:
   per=32//bits; words=(4096+per-1)//per; data=v[pos:pos+4*words]; pos+=4*words; n=struct.unpack_from('<I',v,pos)[0]; pos+=4
  else: n=1; data=None
  for idx in range(n):
   start=pos; ctx=ReadContext(); t=load_many(v[pos:],compressed=False,count=1,little_endian=True,read_context=ctx)[0]; pos+=ctx.offset
   if t.compound['name'].py_str in NAMES:
    if 'states' in t.compound and len(t.compound['states'])!=0: raise ValueError('unexpected state')
    replacements.append((start,pos,replacement))
    if bits:
     mask=(1<<bits)-1; c=0
     for j in range(words):
      word=struct.unpack_from('<I',data,j*4)[0]; slots=min(per,4096-j*per)
      c+=sum(((word>>(bits*i))&mask)==idx for i in range(slots))
     block_count+=c
    else: block_count+=4096
 if pos!=len(v): raise ValueError('trailing data')
 out=v
 for start,end,repl in reversed(replacements): out=out[:start]+repl+out[end:]
 return out,block_count,len(replacements)
