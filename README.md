# General Requirements for All Spiders

1. Make sure you have [Python 2.7](https://www.python.org/downloads) installed
2. Make sure you have the latest version of [lxml](http://lxml.de) installed via `pip install lxml==4.1.0`
3. Make sure you have [pytest](https://docs.pytest.org) installed via `pip install pytest` for unit testing

# Scrape the [BMJ's Doc2Doc Archives](https://web.archive.org/web/20160615105956/http://doc2doc.bmj.com/) in 3 Steps

1. Specify the output file to write results to by editing the `doc2doc.py` file's main entry point, e.g. `Spidey().crawl('doc2doc.csv')`
2. Run the script via command line or terminal `python doc2doc.py` which will create a comma-separated output file
3. To run the unit tests, use `pytest -q doc2doc.py`

# Scrape the [Optimal Health Network (OHN) Live Chat Archives](https://web.archive.org/web/20130129082319/http://www.optimalhealthnetwork.com/Alternative-Health-Live-Chat-Log-Archive-s/196.htm) in 3 Steps

1. Specify the output file to write results to by editing the `ohn.py` file's main entry point, e.g. `Spidey().crawl('ohn.csv')`
2. Run the script via command line or terminal `python ohn.py` which will create a comma-separated output file (unit tests available)
3. To run the unit tests, use `pytest -q ohn.py`