# election_data
## pull election data from govt website using scrapy.

* git clone repo
<p>create a virual env <code>python -m venv venv</code></p>
<p>varies for OS but activate virtual enviroment using following command for windows:</p>
* venv\Scripts\activate
* then pip install -r requirements.txt
# show spiders

<p>--scrapy list</p>
# run spider and save results to csv with timestamp.
<p> -- <code>scrapy crawl election -o -"%(time)s_election.csv"</code></p>
