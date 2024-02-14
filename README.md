# cram-to-text
I had my DNA sequenced and got the results as a CRAM file. I wanted to extract the complete sequence from it but had a hard time finding code that did that. After some investigation, I coded up something that worked for me. I thought it may save others some time so sharing it here. If you find any issues please add a comments so it may help others.

The code scans all positions in each chromosome, then finds the most frequent base in each position and writes it to a text file. It divides each chromosome into chunks and each chunk is written to a separate file. The size of a chunk can be configured by changing the value of BASES_PER_FILE.

## Installing pysam
`python3 -m pip install pysam`

## Running
`python3 cram2text.py`

Enjoy!

### Example file (visualized):
<img src="https://github.com/ofermeshi/cram-to-text/assets/10656539/d2a62d03-371f-466f-a5c6-1fc49b1d76e9" width=70% height=70%>
