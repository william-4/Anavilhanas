import os
from pathlib import Path

BASE1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE2 = Path(__file__).resolve().parent.parent

print(BASE1)
print(BASE2)