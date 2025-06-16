import pandas as pd
import zipfile
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn 
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Importar datos de empleo
file_path = r"C:\Users\santi\OneDrive\Documentos\VSC\TFG\estat_lfsi_emp_a.tsv.gz"
df_employment = pd.read_csv(file_path, sep="\t", compression="gzip")

# Importar datos de deuda pública
debt_file = r"C:\Users\santi\OneDrive\Documentos\VSC\TFG\estat_gov_10dd_edpt1.tsv.gz"
df_debt = pd.read_csv(debt_file, sep="\t", compression="gzip")

# Importar datos del PIB
gdp_file = r"C:\Users\santi\OneDrive\Documentos\VSC\TFG\estat_nama_10_gdp.tsv.gz"
df_gdp = pd.read_csv(gdp_file, sep="\t", compression="gzip")

# Importar datos de inflación
inflation_file = r"C:\Users\santi\OneDrive\Documentos\VSC\TFG\estat_prc_hicp_aind.tsv.gz"
df_inflation = pd.read_csv(inflation_file, sep="\t", compression="gzip")

# Importar datos del coeficiente de Gini
file_path_gini = r'C:\Users\santi\OneDrive\Documentos\VSC\TFG\estat_ilc_di12b.tsv.gz'
df_gini = pd.read_csv(file_path_gini, sep='\t', compression='gzip')

# Importar datos de desempleo
file_path_unemployment = r'C:\Users\santi\OneDrive\Documentos\VSC\TFG\estat_une_rt_a.tsv.gz'
df_unemployment = pd.read_csv(file_path_unemployment, sep='\t', compression='gzip')

# Store all dataframes in a dictionary
dfs = {
    'df_gini': df_gini,
    'df_unemployment': df_unemployment,
    'df_gdp': df_gdp,
    'df_employment': df_employment,
    'df_debt': df_debt,
    'df_inflation': df_inflation
}

years = [str(y) + " " for y in range(2003, 2025)]
selected_countries = ['ES', 'EL', 'IT', 'FR', 'DE', 'AT', 'PT', 'NL']

def reshape_and_split_auto(df):
    id_col = df.columns[0]
    id_vars = [id_col]
    df_long = df.melt(
        id_vars=id_vars,
        value_vars=[col for col in df.columns if col in years],
        var_name="year",
        value_name="value"
    )
    df_long["year"] = df_long["year"].str.strip().astype(int)
    new_cols = id_col.split(",")
    df_long[new_cols] = df_long[id_col].str.split(",", expand=True)
    df_long = df_long.drop(columns=id_col)
    geo_col = [col for col in new_cols if "geo" in col or "geo\\TIME_PERIOD" in col]
    if geo_col:
        df_long = df_long.rename(columns={geo_col[0]: "country"})
    if "country" in df_long.columns:
        df_long = df_long[df_long["country"].isin(selected_countries)]
    return df_long

dfs_long = {name: reshape_and_split_auto(df) for name, df in dfs.items()}

df_employment_long = reshape_and_split_auto(df_employment)
df_unemployment_long = reshape_and_split_auto(df_unemployment)
df_debt_long = reshape_and_split_auto(df_debt)
df_gdp_long = reshape_and_split_auto(df_gdp)
df_inflation_long = reshape_and_split_auto(df_inflation)
df_gini_long = reshape_and_split_auto(df_gini)

# Aplicar filtros
totals_emp = df_employment_long[
    (df_employment_long["sex"] == "T") &
    (df_employment_long["age"] == "Y15-64") &
    (df_employment_long["unit"] == "PC_POP") &
    (df_employment_long["freq"] == "A") &
    (df_employment_long["indic_em"] == "EMP_LFS")
].copy()

totals_unemp = df_unemployment_long[
    (df_unemployment_long["sex"] == "T") &
    (df_unemployment_long["age"] == "Y15-74") &
    (df_unemployment_long["unit"] == "PC_POP") &
    (df_unemployment_long["freq"] == "A")
].copy()

totals_debt_pct = df_debt_long[
    (df_debt_long["freq"] == "A") &
    (df_debt_long["unit"] == "PC_GDP") &
    (df_debt_long["sector"] == "S13") &
    (df_debt_long["na_item"] == "GD")
].copy()

gdp_nominal = df_gdp_long[
    (df_gdp_long["unit"] == "CP_MEUR") &
    (df_gdp_long["na_item"] == "B1G")
].copy()

gdp_real = df_gdp_long[
    (df_gdp_long["unit"] == "CLV10_MEUR") &
    (df_gdp_long["na_item"] == "B1G")
].copy()

totals_inflation = df_inflation_long[
    (df_inflation_long["freq"] == "A") &
    (df_inflation_long["unit"] == "CID_EA") &
    (df_inflation_long["coicop"] == "TOT_X_NRG_FOOD")
].copy()

totals_gini = df_gini_long[
    (df_gini_long["indic_il"] == "GINI_HND")
].copy()

# Renombra la columna 'value' de cada DataFrame antes de mergear para evitar conflictos
totals_emp = totals_emp.rename(columns={"value": "employment_rate"})
totals_unemp = totals_unemp.rename(columns={"value": "unemployment_rate"})
totals_debt_pct = totals_debt_pct.rename(columns={"value": "debt_pct_gdp"})
gdp_nominal = gdp_nominal.rename(columns={"value": "gdp_nominal"})
gdp_real = gdp_real.rename(columns={"value": "gdp_real"})
totals_inflation = totals_inflation.rename(columns={"value": "inflation"})
totals_gini = totals_gini.rename(columns={"value": "gini"})

def select_cols(df, value_col):
    return df[["country", "year", value_col]]

df_merged = totals_emp[["country", "year", "employment_rate"]]
df_merged = df_merged.merge(select_cols(totals_unemp, "unemployment_rate"), on=["country", "year"], how="outer")
df_merged = df_merged.merge(select_cols(totals_debt_pct, "debt_pct_gdp"), on=["country", "year"], how="outer")
df_merged = df_merged.merge(select_cols(gdp_nominal, "gdp_nominal"), on=["country", "year"], how="outer")
df_merged = df_merged.merge(select_cols(gdp_real, "gdp_real"), on=["country", "year"], how="outer")
df_merged = df_merged.merge(select_cols(totals_inflation, "inflation"), on=["country", "year"], how="outer")
df_merged = df_merged.merge(select_cols(totals_gini, "gini"), on=["country", "year"], how="outer")

# Cargar datos de elecciones y gabinetes
zip_path = r"C:\Users\santi\OneDrive\Documentos\VSC\TFG\parlgov-development_csv-utf-8.zip"
with zipfile.ZipFile(zip_path) as z:
    with z.open("view_election.csv") as f:
        df_election = pd.read_csv(f)
    with z.open("view_cabinet.csv") as f:
        df_cabinet = pd.read_csv(f)

df_election['year'] = pd.to_datetime(df_election['election_date'], errors='coerce').dt.year.astype(int)
df_election['country'] = df_election['country_name'].astype(str)
df_cabinet['year'] = pd.to_datetime(df_cabinet['start_date'], errors='coerce').dt.year.astype(int)
df_cabinet['country'] = df_cabinet['country_name'].astype(str)

selected_countries = ['ESP', 'GRC', 'ITA', 'FRA', 'DEU', 'AUT', 'PRT', 'NLD']
years = list(range(2000, 2024))
df_election['election_year'] = pd.to_datetime(df_election['election_date'], errors='coerce').dt.year

mask_pre2008 = (
    (df_election['country_name'].isin(selected_countries)) &
    (df_election['election_type'] == 'parliament') &
    (df_election['election_year'] < 2008)
)
df_pre2008 = df_election[mask_pre2008].copy()
last_pre2008 = (
    df_pre2008.groupby('country_name')['election_year']
    .max()
    .reset_index()
)

df_election_filtered = df_election[
    (df_election['country_name'].isin(selected_countries)) &
    (df_election['election_year'].isin(years))
]
df_prev_elections = pd.merge(
    df_election,
    last_pre2008,
    left_on=['country_name', 'election_year'],
    right_on=['country_name', 'election_year'],
    how='inner'
)
df_election_final = pd.concat([df_election_filtered, df_prev_elections], ignore_index=True)
df_election_final = df_election_final.drop_duplicates()
election_years_for_cabinets = df_election_final['election_year'].unique().tolist()
df_cabinet_final = df_cabinet[
    (df_cabinet['country_name'].isin(selected_countries)) &
    (df_cabinet['year'].isin(election_years_for_cabinets))
]

# Índice de Pedersen
df_election_final = df_election_final.sort_values(['country_name', 'election_year', 'party_id'])
pivot = df_election_final.pivot_table(
    index=['country_name', 'election_year'],
    columns='party_id',
    values='vote_share',
    fill_value=0
).sort_index()

pedersen_results = []
for country, group in pivot.groupby(level=0):
    group_sorted = group.sort_index()
    prev = None
    for year, row in group_sorted.iterrows():
        if prev is not None:
            diff = (row - prev).abs().sum() / 2
            pedersen_results.append({
                'country_name': country,
                'election_year': year,
                'pedersen_index': diff
            })
        prev = row

df_pedersen = pd.DataFrame(pedersen_results)

if isinstance(df_pedersen['election_year'].iloc[0], tuple):
    df_pedersen['election_year'] = df_pedersen['election_year'].apply(lambda x: x[1] if isinstance(x, tuple) else x)
if 'year' in df_pedersen.columns and isinstance(df_pedersen['year'].iloc[0], tuple):
    df_pedersen['year'] = df_pedersen['year'].apply(lambda x: x[1] if isinstance(x, tuple) else x)
else:
    df_pedersen['year'] = df_pedersen['election_year']

country_map = {
    'AUT': 'AT',
    'ESP': 'ES',
    'GRC': 'EL',
    'ITA': 'IT',
    'FRA': 'FR',
    'DEU': 'DE',
    'PRT': 'PT',
    'NLD': 'NL'
}
country_fullname = {
    'AT': 'Austria',
    'ES': 'España',
    'EL': 'Grecia',
    'IT': 'Italia',
    'FR': 'Francia',
    'DE': 'Alemania',
    'PT': 'Portugal',
    'NL': 'Países Bajos'
}
df_pedersen['country_code'] = df_pedersen['country_name'].map(country_map)
df_pedersen['country'] = df_pedersen['country_code'].map(country_fullname)
df_merged['country'] = df_merged['country'].map(country_fullname)
df_pedersen['year'] = df_pedersen['year'].astype(int)
df_merged['year'] = df_merged['year'].astype(int)
df_analysis = pd.merge(df_pedersen, df_merged, on=['country', 'year'], how='left')
df_analysis = df_analysis.rename(columns={'country_name': 'country_short'})
if 'country_code' in df_analysis.columns:
    df_analysis = df_analysis.drop(columns=['country_code'])
cols = df_analysis.columns.tolist()
if 'country' in cols:
    cols.insert(0, cols.pop(cols.index('country')))
    df_analysis = df_analysis[cols]
df_analysis = df_analysis.drop(columns=['year'])

for col in ['employment_rate', 'unemployment_rate', 'debt_pct_gdp', 'gdp_nominal', 'gdp_real', 'inflation', 'gini']:
    df_analysis[col] = pd.to_numeric(df_analysis[col], errors='coerce')

X = df_analysis[['employment_rate', 'unemployment_rate', 'debt_pct_gdp', 'gdp_nominal', 'gdp_real', 'inflation', 'gini']].astype(float)
X = sm.add_constant(X)
y = df_analysis['pedersen_index']
model = sm.OLS(y, X, missing='drop').fit()
print(model.summary())

# Tendencias Temporales y Comparación Entre Países
for var in ['debt_pct_gdp', 'gdp_nominal', 'inflation', 'gini']:
    plt.figure(figsize=(12, 6))
    for country in df_analysis['country'].unique():
        subset = df_analysis[df_analysis['country'] == country]
        plt.plot(subset['election_year'], subset['pedersen_index'], label=f"{country} - Pedersen")
        plt.plot(subset['election_year'], subset[var], label=f"{country} - {var}", linestyle='--')
    plt.title(f'Evolución temporal: Pedersen y {var}')
    plt.xlabel('Año')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()
    plt.show()

stats = df_analysis.groupby('country')['pedersen_index'].agg(['mean', 'std', 'min', 'max'])
print(stats)

df_analysis['period'] = df_analysis['election_year'].apply(lambda x: 'pre-2008' if x < 2008 else 'post-2008')
pre_post = df_analysis.groupby(['country', 'period'])['pedersen_index'].mean().unstack()
print(pre_post)

# Correlaciones y Relaciones Entre Variables
print(df_analysis.corr(numeric_only=True))
for var in ['debt_pct_gdp', 'gini', 'inflation']:
    sns.lmplot(data=df_analysis, x=var, y='pedersen_index', hue='country', aspect=1.5)
    plt.title(f'Pedersen vs {var}')
    plt.show()

scaler = StandardScaler()
for col in ['debt_pct_gdp', 'inflation', 'gini', 'employment_rate']:
    if col in df_analysis.columns:
        df_analysis[f'{col}_z'] = scaler.fit_transform(df_analysis[[col]])

df_analysis['debt_inflation'] = df_analysis['debt_pct_gdp_z'] * df_analysis['inflation_z']
df_analysis['gini_debt'] = df_analysis['gini_z'] * df_analysis['debt_pct_gdp_z']
df_analysis['delta_debt_employment'] = df_analysis['debt_pct_gdp'].diff() * df_analysis['employment_rate'].diff()

for var, label in zip(
    ['debt_inflation', 'gini_debt', 'delta_debt_employment'],
    ['Deuda * Inflación', 'Gini * Deuda', 'ΔDeuda * ΔEmpleo']
):
    sns.lmplot(data=df_analysis, x=var, y='pedersen_index', hue='country', aspect=1.5)
    plt.title(f'Pedersen vs {label}')
    plt.show()

print(df_analysis[['pedersen_index', 'debt_inflation', 'gini_debt', 'delta_debt_employment']].corr())

# Modelos de regresión lineal con interacciones
model_debt_infl = smf.ols('pedersen_index ~ debt_pct_gdp_z * inflation_z', data=df_analysis).fit()
model_gini_debt = smf.ols('pedersen_index ~ gini_z * debt_pct_gdp_z', data=df_analysis).fit()
df_analysis['delta_employment_rate'] = df_analysis.groupby('country')['employment_rate'].diff()
df_analysis['delta_debt_pct_gdp'] = df_analysis.groupby('country')['debt_pct_gdp'].diff()
model_delta = smf.ols('pedersen_index ~ delta_employment_rate * delta_debt_pct_gdp', data=df_analysis).fit()

results = {
    'Deuda*Inflación': model_debt_infl,
    'Gini*Deuda': model_gini_debt,
    'ΔDeuda*ΔEmpleo': model_delta
}
coef_df = pd.DataFrame({c: m.params for c, m in results.items()}).T
cols_to_plot = [col for col in ['debt_pct_gdp_z', 'inflation_z', 'gini_z', 'debt_inflation', 'gini_debt', 'delta_debt_employment', 'delta_employment_rate', 'delta_debt_pct_gdp', 'delta_employment_rate:delta_debt_pct_gdp'] if col in coef_df.columns]
coef_df[cols_to_plot].plot(kind='bar', figsize=(12,6))
plt.title('Comparación de coeficientes por modelo (incluyendo interacciones)')
plt.ylabel('Coeficiente')
plt.xlabel('Modelo')
plt.legend(title='Variable')
plt.tight_layout()
plt.show()

def save_regression_results(df_analysis):
    # Create models
    model_debt_infl = smf.ols('pedersen_index ~ debt_pct_gdp_z * inflation_z', data=df_analysis).fit()
    model_gini_debt = smf.ols('pedersen_index ~ gini_z * debt_pct_gdp_z', data=df_analysis).fit()
    
    # Create delta variables
    df_analysis['delta_employment_rate'] = df_analysis.groupby('country')['employment_rate'].diff()
    df_analysis['delta_debt_pct_gdp'] = df_analysis.groupby('country')['debt_pct_gdp'].diff()
    model_delta = smf.ols('pedersen_index ~ delta_employment_rate * delta_debt_pct_gdp', data=df_analysis).fit()

    # Store results
    results = {
        'Deuda*Inflación': model_debt_infl,
        'Gini*Deuda': model_gini_debt,
        'ΔDeuda*ΔEmpleo': model_delta
    }

    # Create DataFrame for results
    result_df = pd.DataFrame()
    
    # For each model, extract relevant information
    for model_name, model in results.items():
        # Get coefficients
        model_coefs = model.params.rename(f"coef_{model_name}")
        # Get p-values
        model_pvals = model.pvalues.rename(f"pval_{model_name}")
        # Get standard errors
        model_se = model.bse.rename(f"se_{model_name}")
        
        # Combine into DataFrame
        model_df = pd.concat([model_coefs, model_pvals, model_se], axis=1)
        model_df['model'] = model_name
        
        # Add R-squared and other metrics
        metrics = pd.DataFrame({
            'R-squared': [model.rsquared],
            'Adj. R-squared': [model.rsquared_adj],
            'AIC': [model.aic],
            'BIC': [model.bic]
        })
        metrics['model'] = model_name
        
        # Append to result DataFrame
        result_df = pd.concat([result_df, model_df, metrics], ignore_index=True)

    # Save to CSV
    result_df.to_csv('regression_results.csv', index=True)
    print(f"Regression results saved to 'regression_results.csv'")



# PCA de GDP real y Gini
pca_df = df_analysis[['gdp_real', 'gini']].dropna()
scaler = StandardScaler()
pca_scaled = scaler.fit_transform(pca_df)
pca = PCA(n_components=1)
pca_component = pca.fit_transform(pca_scaled)
df_analysis.loc[pca_df.index, 'indice_compuesto_gdp_gini'] = pca_component.flatten()
print("Loadings del primer componente:", pca.components_)
print("Varianza explicada por el primer componente:", pca.explained_variance_ratio_[0])
print(df_analysis[['gdp_real', 'gini', 'indice_compuesto_gdp_gini']].head())

# Subgrupos: Democracias estables y en crisis
subgrupo1 = ['Alemania', 'Austria', 'Países Bajos']
subgrupo2 = ['España', 'Francia', 'Italia', 'Grecia', 'Portugal']

for nombre, paises in {'Democracias estables': subgrupo1, 'Democracias en crisis': subgrupo2}.items():
    print(f"\n--- {nombre} ---")
    df_sub = df_analysis[df_analysis['country'].isin(paises)].dropna()
    if df_sub.empty:
        print("No hay datos para este subgrupo.")
        continue
    X = df_sub[['debt_pct_gdp', 'inflation', 'indice_compuesto_gdp_gini']]
    X = sm.add_constant(X)
    y = df_sub['pedersen_index']
    model = sm.OLS(y, X, missing='drop').fit()
    print(f"R²: {model.rsquared:.2f}, AIC: {model.aic:.1f}, BIC: {model.bic:.1f}")
    print(model.summary().tables[1])
    vif = pd.DataFrame()
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif["variable"] = X.columns
    print(f"\nVIF para {nombre}:\n", vif)

# Gráficos de dispersión por país
sns.lmplot(
    data=df_analysis,
    x='inflation',
    y='pedersen_index',
    hue='country',
    col='country',
    col_wrap=4,
    height=3,
    aspect=1
)
plt.suptitle('Pedersen vs Inflación por país', y=1.02)
plt.show()

sns.lmplot(
    data=df_analysis,
    x='debt_pct_gdp',
    y='pedersen_index',
    hue='country',
    col='country',
    col_wrap=4,
    height=3,
    aspect=1
)
plt.suptitle('Pedersen vs Deuda (% PIB) por país', y=1.02)
plt.show()

sns.lmplot(
    data=df_analysis,
    x='indice_compuesto_gdp_gini',
    y='pedersen_index',
    hue='country',
    col='country',
    col_wrap=4,
    height=3,
    aspect=1
)
plt.suptitle('Pedersen vs Índice Compuesto GDP-Gini por país', y=1.02)
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df_analysis,
    x='country',
    y='indice_compuesto_gdp_gini'
)
plt.title('Distribución del Índice Compuesto GDP-Gini por país')
plt.xlabel('País')
plt.ylabel('Índice Compuesto GDP-Gini')
plt.tight_layout()
plt.show()

# Análisis de surgimiento de nuevos partidos (2008+)
years_post2008 = [y for y in years if y >= 2008]
df_election_filtrado = df_election[
    (df_election['country_name'].isin(selected_countries)) &
    (df_election['election_type'] == 'parliament') &
    (df_election['election_year'].isin(years_post2008))
].copy()
df_election_filtrado = df_election_filtrado.sort_values(['country_name', 'election_year', 'party_id'])
df_election_filtrado['is_new_party'] = False

for country in df_election_filtrado['country_name'].unique():
    country_elections = df_election_filtrado[df_election_filtrado['country_name'] == country]
    for i, year in enumerate(sorted(country_elections['election_year'].unique())):
        if i == 0:
            continue
        prev_year = sorted(country_elections['election_year'].unique())[i-1]
        prev_parties = set(country_elections[country_elections['election_year'] == prev_year]['party_id'])
        curr_mask = (df_election_filtrado['country_name'] == country) & (df_election_filtrado['election_year'] == year)
        df_election_filtrado.loc[curr_mask, 'is_new_party'] = ~df_election_filtrado.loc[curr_mask, 'party_id'].isin(prev_parties)

new_party_stats = (
    df_election_filtrado[df_election_filtrado['is_new_party']]
    .groupby(['country_name', 'election_year'])
    .agg(num_new_parties=('party_id', 'nunique'),
         vote_share_new_parties=('vote_share', 'sum'))
    .reset_index()
)
print(new_party_stats)

cabinet_stats = df_cabinet[
    (df_cabinet['country_name'].isin(new_party_stats['country_name'])) &
    (df_cabinet['year'].isin(new_party_stats['election_year']))
].copy()
cabinet_stats = cabinet_stats.sort_values(['country_name', 'year', 'start_date'])
cabinet_first = cabinet_stats.groupby(['country_name', 'year']).first().reset_index()
merged = pd.merge(
    new_party_stats,
    cabinet_first,
    left_on=['country_name', 'election_year'],
    right_on=['country_name', 'year'],
    how='left'
)
cols_to_show = [
    'country_name', 'election_year', 'num_new_parties', 'vote_share_new_parties',
    'prime_minister', 'party_name_short', 'cabinet_name'
]
print(merged[cols_to_show])

# Cambio de primer ministro y visualizaciones
merged = merged.sort_values(['country_name', 'election_year'])
merged['pm_change'] = merged.groupby('country_name')['prime_minister'].transform(lambda x: x != x.shift(1))

plt.figure(figsize=(8, 5))
sns.boxplot(
    data=merged,
    x='pm_change',
    y='num_new_parties'
)
plt.title('Nuevos partidos y cambio de primer ministro')
plt.xlabel('¿Cambio de primer ministro?')
plt.ylabel('Número de nuevos partidos')
plt.xticks([0, 1], ['No', 'Sí'])
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=merged,
    x='vote_share_new_parties',
    y='num_new_parties',
    hue='pm_change',
    style='country_name',
    s=100
)
plt.title('Nuevos partidos: número y voto vs. cambio de gobierno')
plt.xlabel('Voto total nuevos partidos')
plt.ylabel('Número de nuevos partidos')
plt.legend(title='Cambio de PM')
plt.tight_layout()
plt.show()