# encoding: utf-8

# Program to compute hash of the content, map it with the URL and store it in a file as a key value pair.
# Also, this program validates and save each json document in a separate file.

import sys
import argparse
import datetime
import gzip as gz
import simplejson
import hashlib
import unicodedata
import json


def write_doc(doc, result_file):
    '''
    Takes in CDR document and writes it
    into the result file
    '''

    # write output
    with open(result_file, 'ab') as out:
        out.write(json.dumps(doc) + '\n')


def write_json(jdoc, result_file):
    with open(result_file, 'wb') as out:
        out.write(json.dumps(jdoc) + '\n')


def write_hash(line, result_file):
    with open(result_file, 'ab') as out:
        out.write(line + '\n')


def hash_pair(doc):
    '''
    Takes in CDR document, hashes the raw content
    then hashes the url plus the raw content hash
    '''

    # gather raw content
    raw_content = doc.get('raw_content')

    try:
        # remove leading http(s):// and trailing /
        url = doc.get('url').split("://")[-1]

        if url[-1] == '/':
            url = url[:-1]
    except:
        print("Exception occurred while parsing URL", url)
        return None

    # take sha1 hash of raw_content
    try:
        content_hash = hashlib.sha1(raw_content).hexdigest()

    # in case of a unicode encoding error, encode as 'utf-8'
    except UnicodeEncodeError:
        content_hash = hashlib.sha1(raw_content.encode('utf-8')).hexdigest()

    # generate hash using url and content hash
    hash_pair = hashlib.md5(url+content_hash).hexdigest()

    return hash_pair


def remove_punctuation(text):
    punctutation_cats = {'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'}
    return ''.join(x for x in text if unicodedata.category(x) not in punctutation_cats)


def isValidContent(raw_content):
    fail_keys = ["warning", "return", "string"], ["error", "404"], ["domain", "expired"], ["annonse", "ble", "ikke",
                                                                                           "funnet"], ["no", "se",
                                                                                                       "pudo",
                                                                                                       "encontrar",
                                                                                                       "el", "anuncio",
                                                                                                       "solicitado"]
    flag = True
    content_nopunct = remove_punctuation(raw_content)
    print content_nopunct
    content_list = content_nopunct.split(" ")
    for list in fail_keys:
        counter = 0
        listlen = len(list)
        for item in list:
            if item in content_list:
                counter += 1
        if counter >= listlen:
            flag = False
    if "request ad could not be" in content_nopunct:
        flag = False
    return flag


def isValid(content):
    # Threshold for removing non-compliant documents
    contentLengthThreshold = 150
    if len(content) >= contentLengthThreshold and isValidContent(content):
        return True
    else:
        return False


def main(argv):
    print "CDR De-duplication Phase I"

    desc = 'CDR'
    parser = argparse.ArgumentParser(
        description=desc,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=desc)

    parser.add_argument("--input_file", help="path to the gzip file for testing")
    parser.add_argument("--result_file", help="path to the deduped output file")
    parser.add_argument("--prefix", help="prefix to use for file path")

    args = parser.parse_args()

    # parsed argument for input/result file
    input_file = args.input_file
    result_file = args.result_file
    prefix = args.prefix

    # generate input _ids dictionary
    unique_set = set()

    # capture start time
    start = datetime.datetime.now()
    input_count = 0

    iter = 0
    # iterate over input file to generate identify uniques
    with open(input_file, 'rb') as fp:
        for line in fp:
            doc = json.loads(line)

            # ensure the document is a crawl, not media
            if 'raw_content' in doc:

                # Uncomment this if validation check is required
                if not isValid(doc['raw_content']):
                    continue

                # iterate counter
                input_count += 1

                # generate hash pair
                doc_hash = hash_pair(doc)

                if doc_hash == None:
                    continue

                # if not in unique set, add to set and write to file
                if doc_hash not in unique_set:

                    iter += 1

                    # add to set
                    unique_set.add(doc_hash)

                    id = prefix + str(iter) + '.json'

                    # write hash
                    write_hash(id + ',' + doc_hash, result_file + ".txt")

                    # write json
                    write_json(doc, id)
            else:
                # write output
                write_doc(doc, result_file + ".images")
        fp.close()

    deduped_count = len(unique_set)
    total_dupes = input_count - deduped_count
    end = datetime.datetime.now()
    total_time = end - start

    print(str(total_dupes) + ' duplicates found')
    print('Took ' + str(total_time))



if __name__ == '__main__':
    main(sys.argv)