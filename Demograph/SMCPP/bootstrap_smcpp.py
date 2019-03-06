# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Tue Sep 18 20:39:45 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import random,gzip,time

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('--nr_bootstraps',  type=int, help="nr of bootstraps [20]", default=20)
@click.option("--chunk_size", type=int, help="size of bootstrap chunks [5000000]", default=5000000)
@click.option("--chunks_per_chromosome", type=int,help="nr of chunks to put on one chromosome in the bootstrap [20]", default=20)
@click.option("--nr_chromosomes", type=int, help="nr of chromosomes to write [30]", default=30)
@click.option("--seed", type=int, help="initialize the random number generator")
@click.argument("out_dir_prefix")
@click.argument("filelist", nargs=-1)
def main(nr_bootstraps, chunk_size, chunks_per_chromosome, nr_chromosomes, seed, out_dir_prefix, filelist):
    chunks = []
    offset = 0
    chunks_in_chrom = []
    if not seed:
        seed = int(time.time())
    random.seed(seed)
    print(f'seed: {seed}')
    for file in filelist:
        File = gzip.open(file, 'rb')
        header = File.readline().decode()
        for line in File:
            line = line.decode().strip().split()
            line = [int(x) for x in line]
            pos = line[0] + offset
            offset += line[0]
            chunk_index = (pos - 1) // chunk_size
            if chunk_index > len(chunks_in_chrom)-1:
                chunks_in_chrom.append([])
            chunks_in_chrom[chunk_index].append(line)
    chunks.extend(chunks_in_chrom)

    for bootstrap_id in range(1, nr_bootstraps +1):
        for chr in range(1, nr_chromosomes + 1):
            chr_dir = f'{out_dir_prefix}_{bootstrap_id}'
            if not os.path.exists(chr_dir) : os.makedirs(chr_dir)
            chr_file = f'{chr_dir}/bootstrap_chr{chr}.gz'
            print("writing", chr_file, file=sys.stderr)
            Out = gzip.open(chr_file, 'wb')
            Out.write(header.encode())
            for i in range(chunks_per_chromosome):
                chunk_id = random.randrange(len(chunks))
                for line in chunks[chunk_id]:
                    line = ' '.join([str(x) for x in line]) + '\n'
                    Out.write(line.encode())
if __name__ == '__main__':
    main()
