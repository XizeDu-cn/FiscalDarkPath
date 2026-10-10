"""Count simple structure metrics for benchmark papers (text extracted by pdftotext, non-layout mode).
Usage: python3 -I bench_metrics.py <dir_with_txt> [ids...]
Prints, per paper: max table no., max figure no., reference entries (heuristic), and keyword hits."""
import re, sys, os

d = sys.argv[1]
ids = sys.argv[2:] or sorted(f[:-4] for f in os.listdir(d) if f.endswith('.txt'))

zh_author_year = re.compile(r'^[一-鿿][一-鿿\s、·“”]{0,60}?[（(，,]\s*(19|20)\d{2}[a-z]?\s*[)）]?\s*[：:]')
numbered = re.compile(r'^\s*(?:（(\d+)）|\[(\d+)\]|(\d+)\s*[\.．])\s*\S')
en_start = re.compile(r'^\s*(?:\d+\s*[\.．]\s*|（\d+）|\[\d+\]\s*)?[A-Z][A-Za-zÀ-ÿ\'’\-]+(?:\s[A-Z][a-z]+)?\s*[，,]\s*(?:[A-Z]\.|[A-Z][a-z]+\s[A-Z]\.)')
end_markers = re.compile(r'^(Abstract|Summary|Keywords|JEL|ABSTRACT)\b|^[A-Z][A-Za-z\-]+(\s[A-Za-z\-:,]+){4,}$')

KW = {
    'event': r'事件研究|平行趋势|共同趋势|事前趋势|动态效应',
    'jointp': r'联合检验|联合显著|联合F|联合 F',
    'honest': r'HonestDiD|Rambachan|Roth',
    'trendctrl': r'线性趋势|时间趋势项|趋势项',
    'placebo': r'安慰剂',
    'ebal': r'熵平衡',
    'psm': r'PSM|倾向得分',
    'hetdid': r'Goodman|Bacon|Callaway|Sun和Abraham|Sun 和 Abraham|de Chaisemartin|Borusyak|异质性处理效应|交叠',
    'grpdiff': r'组间系数差异|组间差异检验|费舍尔|Fisher|似无相关|SUEST|Chow|经验p值|经验 p 值',
    'limit': r'局限|不足之处|有待|尚待|未来研究',
    'hedge_may': r'可能',
    'cannot': r'不能',
    'beisuo': r'备索|向作者索取|线上附录|在线附录|网络附录',
}

def ref_count(lines):
    idx = [i for i, l in enumerate(lines) if re.match(r'^\s*参\s*考\s*文\s*献', l)]
    if not idx:
        return None, None
    start = idx[-1] + 1
    seg = []
    for l in lines[start:]:
        if end_markers.match(l.strip()) and seg and len(seg) > 10:
            # stop at English abstract block start ("Summary"/"Abstract") only
            if re.match(r'^(Abstract|Summary|ABSTRACT)\b', l.strip()):
                break
        seg.append(l)
    nums = []
    zh = en = 0
    for l in seg:
        s = l.strip()
        m = numbered.match(s)
        if m:
            n = next(int(x) for x in m.groups() if x)
            if n < 200:
                nums.append(n)
        if zh_author_year.match(s):
            zh += 1
        if en_start.match(s):
            en += 1
    maxnum = max(nums) if nums else 0
    return maxnum, zh + en

print('id\tmax_table\tmax_fig\tref_numbered_max\tref_authoryear\t' + '\t'.join(KW))
for i in ids:
    p = os.path.join(d, i + '.txt')
    if not os.path.exists(p):
        continue
    t = open(p, encoding='utf-8', errors='ignore').read()
    lines = t.splitlines()
    # body = text before the last 参考文献 heading
    cut = [k for k, l in enumerate(lines) if re.match(r'^\s*参\s*考\s*文\s*献', l)]
    body = '\n'.join(lines[:cut[-1]]) if cut else t
    tabs = [int(x) for x in re.findall(r'(?:^|\n)\s*(?:续)?表\s*(\d{1,2})(?!\d)', body)]
    figs = [int(x) for x in re.findall(r'(?:^|\n)\s*图\s*(\d{1,2})(?!\d)', body)]
    mt = max([x for x in tabs if x < 40], default=0)
    mf = max([x for x in figs if x < 40], default=0)
    rn, ra = ref_count(lines)
    kws = [str(len(re.findall(v, body))) for v in KW.values()]
    print(f'{i}\t{mt}\t{mf}\t{rn}\t{ra}\t' + '\t'.join(kws))
