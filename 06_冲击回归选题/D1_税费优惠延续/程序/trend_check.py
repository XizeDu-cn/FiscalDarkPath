"""Pre-trend extrapolation check for annual event studies (base year 2021, post from 2023).
Reads *_全部系数.csv files passed as arguments; prints, per event spec, the pre-period slope,
the post-period coefficients, and their average deviation from the linearly extrapolated pre-trend."""
import csv, sys, collections, math
csv.field_size_limit(10**9)
specs = collections.defaultdict(dict)
meta = {}
for path in sys.argv[1:]:
    with open(path, encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            term = r.get('term') or ''
            if not term.startswith('event_'):
                continue
            try:
                yr = int(term[6:]); b = float(r['coefficient']); se = float(r['std_error'])
            except (ValueError, KeyError):
                continue
            key = (r.get('spec_id'), r.get('exposure'), r.get('outcome'))
            specs[key][yr] = (b, se)
            meta[key] = (r.get('clean_pre_p', ''), r.get('all_pre_p', ''), path.split('/')[-1])
rows = []
for key, d in specs.items():
    if not all(y in d for y in (2018, 2019, 2020)) or not all(y in d for y in (2023, 2024, 2025)):
        continue
    xs = [-3, -2, -1, 0]; ys = [d[2018][0], d[2019][0], d[2020][0], 0.0]
    xb = sum(xs) / 4; yb = sum(ys) / 4
    slope = sum((x - xb) * (y - yb) for x, y in zip(xs, ys)) / sum((x - xb) ** 2 for x in xs)
    icpt = yb - slope * xb
    post = [d[y][0] for y in (2023, 2024, 2025)]
    trend = [icpt + slope * (y - 2021) for y in (2023, 2024, 2025)]
    dev = sum(p - t for p, t in zip(post, trend)) / 3
    rows.append((key, slope, sum(post) / 3, dev, meta[key]))
want = sys.stdin.read().split() if not sys.stdin.isatty() else []
for key, slope, pm, dev, m in sorted(rows, key=lambda r: (r[0][1] or '', r[0][2] or '')):
    if want and key[2] not in want:
        continue
    ratio = dev / pm if pm else float('nan')
    print(f"{key[0]:<12} {key[1]:<6} {key[2][:34]:<34} slope_pre={slope:+.5f} post_mean={pm:+.5f} dev_from_trend={dev:+.5f} share_left={ratio:+.2f} pre_p={m[0][:6]}/{m[1][:6]} [{m[2]}]")
