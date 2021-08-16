import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import time
from glob import glob

from classlogger import Logger
fdir = Path(__file__).resolve().parent

# import pdb; pdb.set_trace()
seq_dir = Path("/vol/ml/yitanzhu/Tempus_Organoid_Data/Processed_RNAseq_Data")
smp_prfx = ["CO-*", "CR-*", "HN-*"]
samples = []
for prfx in smp_prfx:
    samples.extend(sorted(seq_dir.glob(prfx)))

base_outdir = fdir/"quants"
os.makedirs(base_outdir, exist_ok=True)
lg = Logger(base_outdir/"logger")
print_fn = lg.logger.info

# import pdb; pdb.set_trace()
for i, smp in enumerate(samples):
    print_fn(smp)
    outdir = base_outdir/smp.name
    os.makedirs(outdir, exist_ok=True)
    fastq_files = sorted((smp/smp.name).glob("*.fastq.gz"))
    if len(fastq_files) != 2:
        print_fn("\tFound {} files (skip this sample).".format(len(fastq_files)))
        continue
    f1 = fastq_files[0]
    f2 = fastq_files[1]
    os.system("salmon quant -i homo_sapiens_GRCh38_index -l A -1 {} -2 {} -p 8 --validateMappings -o {}".format(f1, f2, outdir))

lg.close_logger()
print("Done.")
