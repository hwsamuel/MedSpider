# Scrape the BMJ's Doc2Doc Data in 5 Steps

1. Make sure you have [Python 2.7](https://www.python.org/downloads) installed
2. Make sure you have the latest version of [lxml](http://lxml.de) installed via `pip install lxml==4.1.0`
3. Verify via unit tests by commenting out `unittest.main()` in the `doc2doc.py` file's main entry point
4. Specify the output file to write results to by editing the `doc2doc.py` file's main entry point, e.g. `s.crawl('doc2doc.csv')`
5. Run the script via command line or terminal `python doc2doc.py` which will create a comma-separated output file