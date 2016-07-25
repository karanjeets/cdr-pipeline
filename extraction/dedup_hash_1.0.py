# encoding: utf-8

# Program to deduplicate document id's based on hash values

import sys
import argparse
import datetime


def main(argv):
    print "CDR De-duplication Phase II"

    desc = 'CDR'
    parser = argparse.ArgumentParser(
        description=desc,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=desc)

    parser.add_argument("--input_file", help="path to the input file")
    parser.add_argument("--result_file", help="path to the deduped output file")

    args = parser.parse_args()

    # parsed argument for input/result file
    input_file = args.input_file
    result_file = args.result_file

    # generate input _ids dictionary
    unique_set = set()

    start = datetime.datetime.now()
    total_count = 0

    # iterate over input file to generate identify uniques
    with open(input_file, 'rb') as fp:
        for line in fp:
            total_count += 1
            values = line.split(",")
            filename = values[0]
            hash = values[1]

            if hash not in unique_set:
                unique_set.add(hash)

                with open(result_file, 'ab') as out:
                    out.write(filename + "\n")


    unique_count = len(unique_set)
    dupe_count = total_count - unique_count
    end = datetime.datetime.now()
    total_time = end - start

    print "Total Count", total_count
    print "Unique Count", unique_count
    print "Duplicate Count", dupe_count

    print 'Took ' + str(total_time)


if __name__ == '__main__':
    main(sys.argv)
