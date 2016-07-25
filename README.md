# CDR Pipeline
Place where Nutch segments are extracted followed by post crawl analysis

--

## Process
A detailed outline of CDR pipeline. You may find some of the steps redundant and it definitely needs improvement. It is a part of learning.
This pipeline was tested for Domain Discovery Eval project wherein we had 12 different types of crawls running and all needs to be dumped and merged into a single file in CDRv2 format.

* Dump all the segments into Common Crawl Dump format using "nutch commoncrawldump" command. As a best practice, loop over all the segments and run this command, so that if it fails in between, you know where to continue from.
* Convert the dumped segments into CDRv2 format as a single file for each crawl using memex_cca_esindex_1.0.py. The new validation checks have been added to the script.
* Now, we have 12 files wherein each line of each file has one JSON document. Some files are large consisting of 180GB and some are 20 GB files
* So, we will be running 12 parallel processes each of which will process one file and does the following (use compute_hash.py and/or compute_valid_hash.py):
 * Check if raw content field is available or not
   * If No, then it is a document. Perform following steps
      * (For 4 files only) - Check if the raw content meets the minimum character length and has valid content
      * Remove leading http(s):// and trailing /
      * Take SHA1 Hash of the html content
      * Take MD5 hash of url and content hash and return that
      * Check if the hash is present in the unique set
         * If No, then
            * Add it to the unique set
            * Write Id, Hash and URL in the result file where Id is a prefix given by user and adding number to it (For eg: A1, A2, A3, etc)
            * Write the document in a separate JSON file with one file per JSON document and name the file with the Id used
         * If Yes, then
            * Increment the counter for duplicate documents in the list
    * If Yes, then it is an image. Perform following steps
      * Append the complete document in a separate result file
* Now, we have 12 result files which have a list of Id, Hash and URL. Get unique URLs from them (use dedup_hash.py):
* Merge all the files into one
* Compare Hash values for uniqueness and get the corresponding Id’s which are nothing but file names
* Loop through all the Id’s and merge JSON files into one (use json_merge.py)

--

### Scripts from external sources
#### Extraction Scripts
* memex_cca_esindex         : Started by Dr. Chris Mattmann and modified by Karanjeet Singh
* cdr_dedupe                : Forked from https://github.com/istresearch/memex-cdr
* cdr_validation            : Forked from https://github.com/istresearch/memex-cdr
