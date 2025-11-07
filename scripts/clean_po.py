import io
from pathlib import Path
p = Path(__file__).resolve().parent.parent / 'locale' / 'en' / 'LC_MESSAGES' / 'django.po'
s = p.read_text(encoding='utf-8')
marker = 'Project-Id-Version: UStore\\n'
# find all occurrences
idxs = [i for i in range(len(s)) if s.startswith(marker, i)]
if len(idxs) < 1:
    print('marker not found; no change')
else:
    # find second occurrence of the header block ("msgid ""\nmsgstr ""\n"Project-Id-Version: UStore\n")
    full_marker = 'msgid ""\nmsgstr ""\n"Project-Id-Version: UStore\\n'
    pos = s.find(full_marker)
    if pos == -1:
        print('full marker not found; no change')
    else:
        # keep from this position onward
        new = s[pos:]
        p.write_text(new, encoding='utf-8')
        print('cleaned', p)
