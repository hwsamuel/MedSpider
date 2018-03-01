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
2. Run the script via command line or terminal `python ohn.py` which will create a comma-separated output file
3. To run the unit tests, use `pytest -q ohn.py`

# Scrape the [eHealth Forum's Ask A Doctor Discussions](https://ehealthforum.com/health/ask_a_doctor_forums.html) in 3 Steps

1. Specify the output file to write results to by editing the `ehealthforum.py` file's main entry point, e.g. `Spidey().crawl('ehealthforum.csv')`
2. Run the script via command line or terminal `python ehealthforum.py` which will create a tab-separated output file
3. To run the unit tests, use `pytest -q ehealthforum.py`

# Scrape the [Doctors Lounge Forum](https://www.doctorslounge.com/forums/) in 3 Steps

1. Specify the output file to write results to by editing the `doctorslounge.py` file's main entry point, e.g. `Spidey().crawl('doctorslounge.csv')`
2. Run the script via command line or terminal `python doctorslounge.py` which will create a tab-separated output file
3. To run the unit tests, use `pytest -q doctorslounge.py`

# Scrape the [Johns Hopkins Breast Center Expert Answers](http://www.hopkinsbreastcenter.org/services/ask_expert/) in 3 Steps

1. Specify the output file to write results to by editing the `hopkins.py` file's main entry point, e.g. `Spidey().crawl('hopkins.csv')`
2. Run the script via command line or terminal `python hopkins.py` which will create a tab-separated output file
3. To run the unit tests, use `pytest -q hopkins.py`

# Scrape the [DocCheck Forum](http://www.doccheck.com/com/ask/) in 5 Steps

1. [Register an account on DocCheck](http://www.doccheck.com/com/account/register/) and make sure that the account is medic-related (the scraper will not work fully without an account)
2. Edit the `doccheck_auth.py` file to enter your DocCheck login credentials
3. Specify the output file to write results to by editing the `doccheck.py` file's main entry point, e.g. `Spidey().crawl('doccheck.csv')`
4. Run the script via command line or terminal `python doccheck.py` which will create a tab-separated output file
5. To run the unit tests, use `pytest -q doccheck.py`

# Scrape the [Health Stack Exchange Q&A Forums](https://health.stackexchange.com/questions?pagesize=50&sort=newest) in 3 Steps

1. Specify the output file and folder name (must exist) to write results to by editing the `healthse.py` file's main entry point, e.g. `Spidey().crawl('healthse.csv', 'healthse')`
2. Run the script via command line or terminal `python healthse.py` which will create a collection of tab-separated output files (please note that Stack Exchange has rate limits): `questions`, `answers`, `question_comments`, `answer_comments`, and `linked_questions`
3. To run the unit tests, use `pytest -q healthse.py`

# Parse the [Health Stack Exchange Q&A Archives](https://archive.org/download/stackexchange) in 3 Steps

1. Download the [`health.stackexchange.com.7z`](https://archive.org/download/stackexchange) archive file and extract it using [7-Zip](http://www.7-zip.org/download.html), it has Ubuntu and Windows versions
2. Note the dataset folder where the extracted XML files are located
3. The `SEParser.py` script can create question pairs using the XML files via `python SEParse.py dataset-folder`. It will save the results to a CSV file within the dataset folder. The script can be modified to perform other extraction and parsing tasks from the XML files.
