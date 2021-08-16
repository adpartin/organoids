import os
from pathlib import Path
import pandas as pd
import numpy as np

from classlogger import Logger
fdir = Path(__file__).resolve().parent

kallisto_dir = Path("/vol/ml/yitanzhu/Tempus_Organoid_Data/Processed_RNAseq_Data/")
salmon_dir = Path("/vol/ml/apartin/projects/organoids/quants")

smp_prfx = ["CO-*", "CR-*", "HN-*"]
samples = []
for prfx in smp_prfx:
    samples.extend(sorted(salmon_dir.glob(prfx)))

base_outdir = fdir/"compare_kallisto_salmon"
os.makedirs(base_outdir, exist_ok=True)
lg = Logger(base_outdir/"logger_compare")
print_fn = lg.logger.info

col_names_mapper = {"Name": "target_id",
                    "Length": "length",
                    "EffectiveLength": "eff_length",
                    "NumReads": "est_counts",
                    "TPM": "tpm"}

# import pdb; pdb.set_trace()
res = []
for i, smp in enumerate(samples):
    print_fn(smp)
    dct = {}
    dct["sample"] = smp.name

    fpath = kallisto_dir/smp.name/"abundance.tsv"
    if fpath.exists():
        df1 = pd.read_csv(fpath, sep="\t")
    else:
        continue

    fpath = fdir/"quants"/smp.name/"quant.sf"
    if fpath.exists():
        df2 = pd.read_csv(fpath, sep="\t")
    else:
        continue

    # print_fn("Kallisto: {}".format(df1.shape))
    # print_fn("Salmon:   {}".format(df2.shape))
    # print(df1[:3])
    # print(df2[:3])

    df2 = df2.rename(columns=col_names_mapper)
    # genes = list(set(df1["target_id"].values).intersection(set(df2["target_id"].values)))

    df = df1.merge(df2, on="target_id", how="inner", suffixes=("_k", "_s")).reset_index(drop=True)
    assert all(df["length_k"].values == df["length_s"].values), "length_k is not equal to length_s"

    # print_fn("Corrcoef of est_counts: {:.3f}".format(np.corrcoef(df["est_counts_k"], df["est_counts_s"])[0, 1]))
    # print_fn("Corrcoef of tpm:        {:.3f}".format(np.corrcoef(df["tpm_k"], df["tpm_s"])[0, 1]))
    dct["corrcoef_counts"] = np.corrcoef(df["est_counts_k"], df["est_counts_s"])[0, 1]
    dct["corrcoef_tpm"] = np.corrcoef(df["tpm_k"], df["tpm_s"])[0, 1]
    res.append(dct)

# import pdb; pdb.set_trace()
res = pd.DataFrame(res)
res.to_csv(base_outdir/"corr_results.csv", sep="\t", index=False)

lg.close_logger()
print("Done.")
