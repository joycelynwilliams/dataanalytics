wget http://hgdownload.soe.ucsc.edu/goldenPath/mm9/encodeDCC/wgEncodeLicrTfbs/wgEncodeLicrTfbsBmarrowCtcfMAdult8wksC57bl6StdAlnRep1.bam
wget http://hgdownload.soe.ucsc.edu/goldenPath/mm9/encodeDCC/wgEncodeLicrTfbs/wgEncodeLicrTfbsBmarrowCtcfMAdult8wksC57bl6StdAlnRep2.bam

samtools sort wgEncodeLicrTfbsBmarrowCtcfMAdult8wksC57bl6StdAlnRep1.bam -o wgEncodeLicrTfbsBmarrowCtcfMAdult8wksC57bl6StdAlnRep1.sorted.bam
samtools sort wgEncodeLicrTfbsBmarrowCtcfMAdult8wksC57bl6StdAlnRep2.bam -o wgEncodeLicrTfbsBmarrowCtcfMAdult8wksC57bl6StdAlnRep2.sorted.bam


##What type of information is stored in bam files like these?
##The .sorted.bam files contain  sequencing data that has been aligned to a reference genome, specifically mouse. The files contain information such as the raw nucleotide sequencing reads ,   quality scores, and the genomic coordinates aligned to the refernece genome. 
