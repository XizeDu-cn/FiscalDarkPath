"""Pre-trend diagnostics for an event-study spec.
Usage: python3 -I pretrend_diag.py <event_data.csv> <covariance.csv> <spec_id> [min_rows]
event_data.csv: rows with spec_id, term, coefficient, std_error, p_value, event_rows,
                first_actual_month, event_index, model_df, n_clusters, all_pre_p.
covariance.csv: square matrix with a leading index column (cluster-robust vcov)."""
import csv, sys
import numpy as np
from scipy import stats

csv.field_size_limit(10**9)
data_path, cov_path, spec = sys.argv[1], sys.argv[2], sys.argv[3]
min_rows = float(sys.argv[4]) if len(sys.argv) > 4 else 200.0

rows = [r for r in csv.DictReader(open(data_path, encoding='utf-8-sig')) if r['spec_id'] == spec]
rows.sort(key=lambda r: int(float(r['event_index'])))
with open(cov_path, encoding='utf-8-sig') as fh:
    rd = csv.reader(fh)
    head = next(rd)[1:]
    V = {}
    for line in rd:
        V[line[0]] = dict(zip(head, map(float, line[1:])))

n_cl = int(float(rows[0]['n_clusters']))
print(f'spec={spec} n={rows[0]["n"]} firms={rows[0]["n_firms"]} clusters={n_cl} reported_all_pre_p={rows[0]["all_pre_p"]}')

pre = [r for r in rows if int(float(r['event_index'])) < 0]
post = [r for r in rows if int(float(r['event_index'])) >= 0]

def wald(terms):
    b = np.array([float(next(r for r in rows if r['term'] == t)['coefficient']) for t in terms])
    S = np.array([[V[a][c] for c in terms] for a in terms])
    w = float(b @ np.linalg.solve(S, b))
    k = len(terms)
    return w, k, 1 - stats.chi2.cdf(w, k), 1 - stats.f.cdf(w / k, k, n_cl - 1)

def lincomb(terms, weights):
    b = np.array([float(next(r for r in rows if r['term'] == t)['coefficient']) for t in terms])
    S = np.array([[V[a][c] for c in terms] for a in terms])
    w = np.array(weights)
    est = float(w @ b); se = float(np.sqrt(w @ S @ w))
    return est, se, 2 * (1 - stats.norm.cdf(abs(est / se)))

print('\n-- pre-period coefficients')
for r in pre:
    print(f"{r['term']:<11} {r['first_actual_month']} rows={float(r['event_rows']):>7.0f} b={float(r['coefficient']):+.4f} se={float(r['std_error']):.4f} p={float(r['p_value']):.3f}")

pt = [r['term'] for r in pre]
w, k, pc, pf = wald(pt)
print(f'\nall pre ({k} terms): W={w:.2f} chi2 p={pc:.4f} F p={pf:.4f}')

keep = [r['term'] for r in pre if float(r['event_rows']) >= min_rows]
drop = [r['first_actual_month'] for r in pre if float(r['event_rows']) < min_rows]
w2, k2, pc2, pf2 = wald(keep)
print(f'pre terms with >= {min_rows:.0f} rows ({k2} terms; dropped {drop}): chi2 p={pc2:.4f} F p={pf2:.4f}')

print('\n-- leave-one-out joint p (chi2), largest increases first')
loo = []
for t in pt:
    ts = [x for x in pt if x != t]
    loo.append((wald(ts)[2], t))
for p, t in sorted(loo, reverse=True)[:6]:
    r = next(r for r in rows if r['term'] == t)
    print(f"drop {t:<11} ({r['first_actual_month']}, rows={float(r['event_rows']):.0f}) -> p={p:.4f}")

# linear pre-trend: OLS slope of pre coefficients on event index (base period coefficient = 0 is excluded)
x = np.array([int(float(r['event_index'])) for r in pre], dtype=float)
for label, sel in (('all pre', pt), (f'pre rows>={min_rows:.0f}', keep)):
    xs = np.array([int(float(next(r for r in rows if r['term'] == t)['event_index'])) for t in sel], dtype=float)
    xc = xs - xs.mean()
    wts = xc / (xc @ xc)
    est, se, p = lincomb(sel, wts)
    mest, mse, mp = lincomb(sel, np.ones(len(sel)) / len(sel))
    print(f'\n{label}: OLS slope per period={est:+.5f} (se {se:.5f}, p={p:.3f}); mean pre coef={mest:+.4f} (se {mse:.4f}, p={mp:.3f})')

# post means
ptm = [r['term'] for r in post]
est, se, p = lincomb(ptm, np.ones(len(ptm)) / len(ptm))
print(f'\nmean of all post coefs ({len(ptm)}): {est:+.4f} (se {se:.4f}, p={p:.4f})')
first = [r['term'] for r in post if int(float(r['event_index'])) < 6]
if first:
    est, se, p = lincomb(first, np.ones(len(first)) / len(first))
    print(f'mean of first {len(first)} post coefs: {est:+.4f} (se {se:.4f}, p={p:.4f})')
print('\n-- post coefficients')
for r in post:
    print(f"{r['term']:<11} {r['first_actual_month']} rows={float(r['event_rows']):>7.0f} b={float(r['coefficient']):+.4f} se={float(r['std_error']):.4f} p={float(r['p_value']):.3f}")
