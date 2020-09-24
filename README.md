# election_data
## pull election data from govt website using scrapy.

### clone repo
<p>create a virual env <code>python -m venv venv</code></p>
<p>varies for OS but activate virtual enviroment using following command for windows:</p>
<code>venv\Scripts\activate</code>
<code>pip install -r requirements.txt</code>

# show spiders

<p>--scrapy list</p>
<p>run spider and save results to csv with timestamp.</p>
<p> -- <code>scrapy crawl election -o -"%(time)s_election.csv"</code></p>
