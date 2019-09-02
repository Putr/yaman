import subprocess
from pprint import pprint

originId = 9
out = subprocess.check_output(['qdbus', 'org.kde.yakuake', '/yakuake/sessions', 'terminalIdsForSessionId', str(originId)])

out = str(out, 'utf-8').strip()
pprint(out)
