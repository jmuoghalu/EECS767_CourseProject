# EECS767_CourseProject

## Instructions for Offline Searching

1. Navigate into the source directory

2. To run **basic searching**, run the following command:

        python3 step4_offline_driver.py

3. To run **term proximity searching**, run the following command:

        python3 step5_offline_driver.py

4. To run **relevance feedback searching**, run the following command:

        python3 step6_offline_driver.py

Instructions for submitting queries are printed to the terminal at runtime.



## The Online Version of This Search Engine Is Available [Here.](https://people.eecs.ku.edu/~j286m692/eecs767_webfiles/ "Group2 Search Engine")




## Running the Document Processor and Creating an Inverted Index

1. Place a folder of HTML documents in the **_file_cache/unprocessed/_** directory.

2. Let the name of this folder be **_customFolder_**.

3. Navigate into the **source** directory.

4. Open a Python terminal:

        python

5. Run the follwing commands:

        import docproc, indexer

        dp = docproc.DocProcessor()
        dp.runDocProc("../file_cache/unprocessed/customFolder")
        iic = indexer.InvertedIndex()
        iic.createInvertedIndex("../file_cache/processed/customFolder")

    The new inverted index will be written as **_data_** directory as **_customFolder\_index.txt_**
