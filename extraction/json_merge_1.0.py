# encoding: utf-8

# Program to merge all Json documents into one file

import sys
import argparse
import gzip


def main(argv):
    print "CDR De-duplication Phase III"

    desc = 'CDR'
    parser = argparse.ArgumentParser(
        description=desc,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=desc)

    parser.add_argument("--input_file", help="path to the input file")
    parser.add_argument("--result_file", help="path to the merged output file")

    args = parser.parse_args()

    # parsed argument for input/result file
    input_file = args.input_file
    result_file = args.result_file

    docs = []
    iter = 0

    with open(input_file, 'rb') as fp:
        for line in fp:
            iter += 1
            filename = line.strip()
            print "Processing ", filename
            with open(filename, 'rb') as jfile:
                doc = jfile.read().strip()

            if not doc:
                continue
            else:
                docs.append(doc)

            if iter % 1000 == 0:
                with gzip.open(result_file, 'a') as out:
                    out.write("\n".join(docs) + "\n")
                docs = []

    print "\nProcessed ", iter, " documents"


if __name__ == '__main__':
    main(sys.argv)
