"""Reproduce Task 3 exploratory analysis from the included World Bank panel."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'south_asia_wdi_2000_2024.csv'
FIG = ROOT / 'figures'
OUT = ROOT / 'outputs'
FIG.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

COUNTRIES = ['Bangladesh', 'India', 'Nepal', 'Pakistan', 'Sri Lanka']
df = pd.read_csv(DATA)
expected = 5 * 25
assert len(df) == expected, f'Expected {expected} rows; found {len(df)}'
assert df[['gdp_pc_2015_usd', 'life_expectancy_years']].notna().all().all()
assert not df.duplicated(['country_code', 'year']).any()
assert (df.gdp_pc_2015_usd > 0).all()
assert df.life_expectancy_years.between(0, 120).all()
assert set(df.country) == set(COUNTRIES)

summary = []
for country, g in df.groupby('country', sort=False):
    g = g.sort_values('year').set_index('year')
    first, last = g.loc[2000], g.loc[2024]
    gdp_change = (last.gdp_pc_2015_usd / first.gdp_pc_2015_usd - 1) * 100
    cagr = ((last.gdp_pc_2015_usd / first.gdp_pc_2015_usd) ** (1 / 24) - 1) * 100
    summary.append({
        'country': country,
        'gdp_pc_2000': first.gdp_pc_2015_usd,
        'gdp_pc_2024': last.gdp_pc_2015_usd,
        'gdp_pc_change_pct': gdp_change,
        'gdp_pc_cagr_pct': cagr,
        'life_2000': first.life_expectancy_years,
        'life_2024': last.life_expectancy_years,
        'life_change_years': last.life_expectancy_years - first.life_expectancy_years,
        'within_country_pearson_r': g.gdp_pc_2015_usd.corr(g.life_expectancy_years),
    })
summary = pd.DataFrame(summary)
summary.to_csv(OUT / 'country_2000_2024_summary.csv', index=False, float_format='%.4f')
descriptive = df[['gdp_pc_2015_usd', 'life_expectancy_years']].describe()
descriptive.to_csv(OUT / 'pooled_descriptive_statistics.csv', float_format='%.4f')
pooled_r = df.gdp_pc_2015_usd.corr(df.life_expectancy_years)
print(f'Observations: {len(df)}; missing: {int(df.isna().sum().sum())}; pooled Pearson r: {pooled_r:.4f}')
print('Pooled descriptive statistics:\n', descriptive.round(2))
print(summary.to_string(index=False, float_format=lambda x: f'{x:.2f}'))

sns.set_theme(style='whitegrid', context='notebook')
palette = dict(zip(COUNTRIES, sns.color_palette('colorblind', n_colors=5)))
fig, ax = plt.subplots(figsize=(9.4, 4.9))
for country, g in df.groupby('country'):
    ax.plot(g.year, g.gdp_pc_2015_usd / 1000, marker='o', markersize=3.2, lw=2, label=country, color=palette[country])
ax.set(title='Real GDP per capita, 2000–2024', xlabel='Year', ylabel='Constant 2015 US$ (thousands)')
ax.legend(ncol=3, frameon=False, loc='upper left'); ax.set_xlim(2000, 2024)
fig.tight_layout(); fig.savefig(FIG / 'gdp_per_capita_trends.png', dpi=190, bbox_inches='tight'); plt.close(fig)

fig, ax = plt.subplots(figsize=(9.4, 4.9))
for country, g in df.groupby('country'):
    ax.plot(g.year, g.life_expectancy_years, marker='o', markersize=3.2, lw=2, label=country, color=palette[country])
ax.set(title='Life expectancy at birth, 2000–2024', xlabel='Year', ylabel='Years')
ax.legend(ncol=3, frameon=False, loc='lower right'); ax.set_xlim(2000, 2024)
fig.tight_layout(); fig.savefig(FIG / 'life_expectancy_trends.png', dpi=190, bbox_inches='tight'); plt.close(fig)

fig, ax = plt.subplots(figsize=(8.8, 5.2))
for country, g in df.groupby('country'):
    ax.scatter(g.gdp_pc_2015_usd / 1000, g.life_expectancy_years, s=34, alpha=.75,
               label=country, color=palette[country], edgecolor='white', linewidth=.35)
    last = g[g.year == 2024].iloc[0]
    ax.scatter(last.gdp_pc_2015_usd / 1000, last.life_expectancy_years, s=100, marker='*',
               color=palette[country], edgecolor='black', linewidth=.55, zorder=4)
ax.set(title='GDP per capita and life expectancy across observations',
       xlabel='GDP per capita (constant 2015 US$ thousands)', ylabel='Life expectancy at birth (years)')
ax.legend(frameon=False, ncol=2, loc='lower right', title='Country; star = 2024')
fig.tight_layout(); fig.savefig(FIG / 'gdp_life_scatter.png', dpi=190, bbox_inches='tight'); plt.close(fig)

fig, ax = plt.subplots(figsize=(8.8, 4.8))
plot = summary.sort_values('gdp_pc_change_pct', ascending=True)
ax.barh(plot.country, plot.gdp_pc_change_pct, color=[palette[c] for c in plot.country])
ax.set(title='Change in real GDP per capita, 2000–2024', xlabel='Cumulative change (%)', ylabel='')
for i, value in enumerate(plot.gdp_pc_change_pct):
    ax.text(value + 2, i, f'{value:.0f}%', va='center', fontsize=9)
ax.set_xlim(0, max(plot.gdp_pc_change_pct) * 1.18)
fig.tight_layout(); fig.savefig(FIG / 'gdp_pc_change.png', dpi=190, bbox_inches='tight'); plt.close(fig)
