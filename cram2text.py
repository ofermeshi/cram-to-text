import pysam

base_path = '/path/to/cram/directory'
cram_path = base_path + 'file_name.cram'
crai_path = base_path + 'file_name.cram.crai'
out_path = base_path + '/sequence'

WINDOW = 1000
BASES_PER_FILE = 1e6
def fetch_seq(cram_file, region, length, max_buf=1e6):
  def save_seq(seq, seq_begin):
    seq_end = seq_begin + len(seq) - 1
    filename = f"{out_path}/{region}_{seq_begin}_{seq_end}.txt"
    print(f"Writing {filename}...")
    with open(filename, "w") as f:
      for base in seq:
        f.write(base)
    f.close()

  seq = []
  seq_begin = 0
  begin = 0
  end = begin + WINDOW - 1
  while True:
    if end >= length:
      end = length - 1
    if begin >= end:
      break
    positions = cram_file.pileup(contig=region, start=begin, stop=end)
    for position in positions:
      ref_pos = position.reference_pos
      if ref_pos < begin or ref_pos > end:
        continue
      base_count = { 'A': 0, 'C': 0, 'G': 0, 'T': 0 }
      for read in position.pileups:
        if read.query_position is None:
          continue
        base = read.alignment.query_sequence[read.query_position]
        base_count[base] += 1
      most_freq_base = max(base_count, key=base_count.get)
      seq.append(most_freq_base)
      if len(seq) >= max_buf:
        save_seq(seq, seq_begin)
        seq_begin = seq_begin + len(seq)
        seq = []
    begin = end + 1
    end = begin + WINDOW - 1
  # Save last window
  save_seq(seq, seq_begin)


# Main starts here
# Open the CRAM file
print(f"Opening {cram_path}...", flush=True)
cram_file = pysam.AlignmentFile(cram_path, "rc",
                                index_filename=crai_path)

# Find region lengths
print(f"Index: {cram_file.check_index()}")
stats = cram_file.get_index_statistics()
ref_lengths = cram_file.lengths
region_lengths = {}
for stat, length in zip(stats, ref_lengths):
  region_lengths[stat.contig] = length

chromosomes = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY', 'chrM']
for chr in chromosomes:
  print("Chromosome:", chr)
  chr_len = region_lengths[chr]
  print("Length:", chr_len)
  fetch_seq(cram_file, chr, chr_len, max_buf=BASES_PER_FILE)

# Close the CRAM file
cram_file.close()
