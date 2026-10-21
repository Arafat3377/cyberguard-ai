import numpy as np
import pandas as pd
from pathlib import Path
rng=np.random.default_rng(42)
rows=[]
classes=['Normal Activity','Suspicious Login','Port Scanning','Brute Force','Abnormal Traffic','Malware-like Activity']
for label in classes:
    n=250
    if label=='Normal Activity': vals=(rng.poisson(1,n), rng.normal(20000,5000,n), rng.poisson(30,n), rng.poisson(40,n), rng.binomial(1,.05,n))
    elif label=='Suspicious Login': vals=(rng.poisson(6,n), rng.normal(25000,7000,n), rng.poisson(35,n), rng.poisson(70,n), rng.binomial(1,.2,n))
    elif label=='Port Scanning': vals=(rng.poisson(2,n), rng.normal(30000,8000,n), rng.poisson(220,n), rng.poisson(200,n), rng.binomial(1,.25,n))
    elif label=='Brute Force': vals=(rng.poisson(25,n), rng.normal(18000,5000,n), rng.poisson(45,n), rng.poisson(150,n), rng.binomial(1,.4,n))
    elif label=='Abnormal Traffic': vals=(rng.poisson(4,n), rng.normal(180000,60000,n), rng.poisson(300,n), rng.poisson(400,n), rng.binomial(1,.25,n))
    else: vals=(rng.poisson(10,n), rng.normal(300000,90000,n), rng.poisson(180,n), rng.poisson(250,n), rng.binomial(1,.45,n))
    for a,b,c,d,e in zip(*vals): rows.append([max(0,a),max(100,b),max(1,c),max(1,d),e,label])
df=pd.DataFrame(rows,columns=['failed_logins','bytes','connections','requests','unusual_hour','label'])
out=Path(__file__).resolve().parent/'security_events.csv'; df.to_csv(out,index=False); print(out, len(df))
