from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ml_engine.pipeline import predict
sample={'failed_logins':25,'bytes':18000,'connections':45,'requests':150,'unusual_hour':1}
print(predict(sample))
