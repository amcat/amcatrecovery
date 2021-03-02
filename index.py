import tarfile
from pathlib import Path
out = Path.cwd() / "export" / "articles"
for f in out.glob("project_*.tgz"):
    with tarfile.open(f) as tf:
        member = tf.getmember("manifest.json")
        
        f=tf.extractfile(member)
        content=f.read()
        print(content)
        break
    
    
