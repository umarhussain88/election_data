# election_data
pull election data from govt website using scrapy.

git clone repo
create a virual env python -m venv venv
varies for OS but activate virtual enviroment using following command for windows:

venv\Scripts\activate
then pip install -r requirements.txt
#show spiders
scrapy list
#run spider and save results to csv with timestamp.
scrapy crawl election -o -"%(time)s_election.csv"
