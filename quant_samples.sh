#!/bin/bash

# kallisto quant -i ../kallisto/transcriptome_indices/Ensembl_Transcriptomes_v104/transcriptome.idx -o outputfolder --plaintext fastq_file1 fastq_file2

seq_data_date=Sequencing_Data_20210326
dir_name=CO-173

salmon quant -i homo_sapiens_GRCh38_index -l A -1 ./data/Sequencing_Data_20210326/CO-173/RNA/FastQ/CO-173_1.fastq.gz -2 ./data/Sequencing_Data_20210326/CO-173/RNA/FastQ/CO-173_3.fastq.gz -p 8 --validateMappings -o quants/${dir_name}

##!/bin/bash
#for fn in data/DRR0161{25..40};
#do
#  samp=`basename ${fn}`
#  echo "Processing sample ${samp}"
#  salmon quant -i athal_index -l A \
#           -1 ${fn}/${samp}_1.fastq.gz \
#           -2 ${fn}/${samp}_2.fastq.gz \
#           -p 8 --validateMappings -o quants/${samp}_quant
#done
