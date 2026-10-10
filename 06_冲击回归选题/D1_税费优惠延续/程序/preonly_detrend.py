"""Pre-period-only linear detrending for annual event studies (HonestDiD inputs, reference year 2022 = 0).
For each outcome: fit an OLS line through the pre-period coefficients (2018-2021) and the reference
point (2022, 0), extrapolate it to 2023-2025, and report the average deviation of the post coefficients
from that line, with a standard error from the full event-study covariance.
Also prints the original static coefficient and the full-sample joint-trend coefficient for comparison.
Usage: python3 -I preonly_detrend.py <honest_inputs_dir> <annual34_csv>"""
import csv, json, os, sys
import numpy as np
from scipy import stats

hdir, tab = sys.argv[1], sys.argv[2]
static = {r['spec_id']: r for r in csv.DictReader(open(tab, encoding='utf-8-sig'))}

def star(p):
    return '***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.1 else ''

out = []
for spec in sorted(os.listdir(hdir)):
    d = os.path.join(hdir, spec)
    meta = json.load(open(os.path.join(d, 'metadata.json'), encoding='utf-8'))
    beta = list(csv.DictReader(open(os.path.join(d, 'beta.csv'), encoding='utf-8-sig')))
    years = [int(r['year']) for r in beta]
    b = np.array([float(r['estimate']) for r in beta])
    with open(os.path.join(d, 'sigma.csv'), encoding='utf-8-sig') as fh:
        rd = csv.reader(fh); head = next(rd)[1:]
        S = np.array([[float(x) for x in line[1:]] for line in rd])
    pre_idx = [i for i, y in enumerate(years) if y < 2022]
    post_idx = [i for i, y in enumerate(years) if y > 2022]
    # design for OLS line through pre points + (2022, 0): slope/intercept are linear in beta_pre
    xs = np.array([years[i] - 2022 for i in pre_idx] + [0.0])
    X = np.column_stack([np.ones(len(xs)), xs])
    H = np.linalg.solve(X.T @ X, X.T)          # 2 x (npre+1); last column multiplies the fixed 0
    H = H[:, :-1]                               # drop the reference column (its value is 0)
    w = np.zeros(len(years))
    npost = len(post_idx)
    for i in post_idx:
        w[i] += 1.0 / npost
        k = years[i] - 2022
        # subtract (a + b k)/npost, where (a, b) = H @ beta_pre
        for j, pi in enumerate(pre_idx):
            w[pi] -= (H[0, j] + H[1, j] * k) / npost
    dev = float(w @ b); se = float(np.sqrt(w @ S @ w)); p = 2 * (1 - stats.norm.cdf(abs(dev / se)))
    lp = np.zeros(len(years)); lp[post_idx] = 1.0 / npost
    pm = float(lp @ b); pse = float(np.sqrt(lp @ S @ lp)); pp = 2 * (1 - stats.norm.cdf(abs(pm / pse)))
    slope_w = np.zeros(len(years)); slope_w[pre_idx] = H[1]
    sl = float(slope_w @ b); slse = float(np.sqrt(slope_w @ S @ slope_w)); slp = 2 * (1 - stats.norm.cdf(abs(sl / slse)))
    st = static.get(spec, {})
    co = float(st.get('coefficient_original', 'nan')); po = float(st.get('p_value_original', 'nan'))
    ct = float(st.get('coefficient_lineartrend', 'nan')); pt = float(st.get('p_value_lineartrend', 'nan'))
    out.append((meta['outcome'], co, po, ct, pt, pm, pp, sl, slp, dev, se, p, st.get('all_pre_p', '')))

print(f"{'outcome':<34} {'original':>13} {'joint-trend':>13} {'post avg(ref22)':>16} {'pre slope':>14} {'pre-only detrended dev (se)':>30} all_pre_p")
for o, co, po, ct, pt, pm, pp, sl, slp, dev, se, p, ap in out:
    print(f"{o[:34]:<34} {co:+.4f}{star(po):<3}   {ct:+.4f}{star(pt):<3}   {pm:+.4f}{star(pp):<3}   {sl:+.5f}{star(slp):<3}   {dev:+.4f}{star(p):<3} ({se:.4f}) p={p:.3f}   {float(ap) if ap else float('nan'):.3f}")
