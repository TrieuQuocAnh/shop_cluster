"""
Evaluate clustering configurations across rule-only vs rule+RFM,
binary vs weighted rule encodings, and Top-K small vs Top-K large.

Usage: run this script from the repo root (where `data/processed` lives).
It saves `data/processed/experiments_results.csv` with per-config metrics.
"""
import os
from itertools import product
import time
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

from cluster_library import DataCleaner, BasketPreparer, AssociationRulesMiner


def build_invoice_itemsets(df):
    grouped = df.groupby('InvoiceNo')['Description'].apply(lambda s: set(s.values))
    return grouped.to_dict()


def build_invoice_customer_map(df):
    inv_cust = df.groupby('InvoiceNo')['CustomerID'].first()
    return inv_cust.to_dict()


def map_rules_to_customers(rules, invoice_itemsets, invoice_customer_map):
    # rules: DataFrame with 'antecedents' as frozenset
    # returns DataFrame: index customerID, columns rule_i -> counts of invoices where antecedent matched
    invoices = list(invoice_itemsets.keys())
    cust_rule_counts = {}
    # prepare customer invoice list
    cust_invoices = {}
    for inv, cust in invoice_customer_map.items():
        cust_invoices.setdefault(cust, []).append(inv)

    for i, row in rules.iterrows():
        ants = set(row['antecedents'])
        matched_invoices = [inv for inv in invoices if ants.issubset(invoice_itemsets[inv])]
        inv_to_cust = {}
        for inv in matched_invoices:
            cust = invoice_customer_map.get(inv)
            if cust is None:
                continue
            inv_to_cust.setdefault(cust, 0)
            inv_to_cust[cust] += 1
        cust_rule_counts[f'rule_{i}'] = inv_to_cust

    customers = sorted(cust_invoices.keys())
    df = pd.DataFrame(index=customers)
    for col, counts in cust_rule_counts.items():
        df[col] = df.index.map(lambda c: counts.get(c, 0))
    df.index.name = 'CustomerID'
    return df


def run_experiments(data_path='data/processed/cleaned_uk_data.csv',
                    output_path='data/processed/experiments_results.csv',
                    ks=(50, 200), encodings=('binary', 'weighted'), include_rfms=(False, True),
                    n_clusters=3, min_support=0.01):

    df_all = pd.read_csv(data_path, parse_dates=['InvoiceDate'])

    # prepare invoice-level basket boolean
    bp = BasketPreparer(df_all)
    basket = bp.create_basket()
    basket_bool = bp.encode_basket(threshold=1).astype(bool)

    invoice_itemsets = build_invoice_itemsets(df_all)
    invoice_customer_map = build_invoice_customer_map(df_all)

    results = []

    for k, enc, use_rfm in product(ks, encodings, include_rfms):
        config_name = f'K={k}|enc={enc}|rfm={use_rfm}'
        print(f'Running {config_name}')
        t0 = time.time()

        miner = AssociationRulesMiner(basket_bool=basket_bool)
        fi = miner.mine_frequent_itemsets(min_support=min_support, use_colnames=True)
        rules = miner.generate_rules(metric='lift', min_threshold=1.0)
        if rules.empty:
            print('No rules found, skipping')
            continue

        rules = miner.add_readable_rule_str()
        rules = rules.sort_values(['lift', 'confidence'], ascending=False).reset_index(drop=True)
        topk = rules.head(k)

        cust_rule_df = map_rules_to_customers(topk, invoice_itemsets, invoice_customer_map)

        if enc == 'binary':
            X_rules = (cust_rule_df > 0).astype(int)
        else:
            # weighted: normalize by customer total invoices to reduce bias
            cust_invoice_counts = df_all.groupby('CustomerID')['InvoiceNo'].nunique()
            X_rules = cust_rule_df.div(cust_invoice_counts, axis=0).fillna(0)

        X = X_rules.copy()
        if use_rfm:
            dc = DataCleaner(data_path=None)
            dc.df_uk = df_all
            rfm = dc.compute_rfm()
            rfm = rfm.set_index('CustomerID')
            rfm = rfm.reindex(X.index).fillna(0)
            X = pd.concat([X, rfm[['Recency', 'Frequency', 'Monetary']]], axis=1)

        # drop customers with all-zero features
        nonzero_mask = (X.abs().sum(axis=1) > 0)
        X = X[nonzero_mask]
        if X.shape[0] < n_clusters:
            print('Not enough customers after filtering, skipping')
            continue

        scaler = StandardScaler()
        Xs = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(Xs)

        sil = silhouette_score(Xs, labels) if len(set(labels)) > 1 else np.nan
        db = davies_bouldin_score(Xs, labels) if len(set(labels)) > 1 else np.nan
        ch = calinski_harabasz_score(Xs, labels) if len(set(labels)) > 1 else np.nan

        cluster_sizes = pd.Series(labels).value_counts().sort_index().to_dict()

        # aggregate RFM by cluster if available
        cluster_rfm = None
        if use_rfm:
            tmp = pd.DataFrame({'label': labels}, index=X.index)
            rfm_stats = rfm.reindex(tmp.index).join(tmp)
            cluster_rfm = rfm_stats.groupby('label')[['Recency','Frequency','Monetary']].mean().to_dict()

        results.append({
            'config': config_name,
            'k': k,
            'encoding': enc,
            'use_rfm': use_rfm,
            'n_customers': X.shape[0],
            'silhouette': sil,
            'davies_bouldin': db,
            'calinski_harabasz': ch,
            'cluster_sizes': cluster_sizes,
            'cluster_rfm': cluster_rfm,
            'runtime_sec': time.time() - t0,
        })

    out_df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    out_df.to_csv(output_path, index=False)
    print('Saved experiment results to', output_path)
    # print summary sorted by silhouette desc
    print(out_df.sort_values('silhouette', ascending=False)[['config','n_customers','silhouette','davies_bouldin','calinski_harabasz']])


if __name__ == '__main__':
    run_experiments()
