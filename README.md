# wikiViz

Check out the [web app](https://ush19-wikiviz-front-end-implementationwikiviz-app-jvy70i.streamlit.app/)!


##  Inspiration 
Inspiration for this project was drawn from [@terrence.png](https://www.tiktok.com/@terrence.png) on TikTok who maps two Wikipedia pages to each other with only the page's content and context. Combined with my interest in network science, I thought it'd be interesting to build a program to build the connections from nodes (Wikipedia pages) and the links which would lead from Wikipedia page A to Wikipedia page B. 

##  Goals
- Calculate the shortest path between two Wikipedia pages, if any. 
- Return degrees of separation between Wikipedia pages if such a path exists.
- 

##  Questions?
Email me at palakurthisusheel@gmail.com

##  Connect with me!
Connect with me on [LinkedIn](https://www.linkedin.com/in/psusheel/)!

##  Future implementations
- Fix direction of network graph to go specifically from A --> node --> node --> B, instead of A --> node --> node <-- B (currently algorithm works in the latter direction), likely caused by the placement of page search B as the second elemnent in the titles list which causes the algorithm to find all links on that page (in hindsight, not an issue but most likely not the proper way to go about finding separation)
- Develop network visualization (c'mon Susheel, hence the name wikiVIZ) from degrees of separation
- Reduce scope of links by removing links which aren't in the direct Wikipedia article
- Simplify how nodes are combined from searches A and B
- Implement other networkx functions, after review of network science and analysis
- After code is successfully run, add degrees of separation and which links 
      **[implemented, 5dec2022]**
- Add failure messages to a log 
- Front end for this Python application (Streamlit? Shiny?)
      **[implemented, 17dec2022]**
- After making UI for the Python Streamlit app, adding to logs isn't working -- TODO: FIX
- Beautify front end for Python Streamlit app
- Make sure errors don't appear in times of too many API requests on Streamlit app
- Control number of users on Streamlit app 
- Replicate project in R, with WikipediR and igraph and implement front end for R application (Shiny?)
- Reinvent the wheel by developing new logic and functionality for getting Wikipedia links (API - no. possibly BeautifulSoup - yes) and calculating shortest path -- TODO: use wikimedia API instead of BeautifulSoup or Scrapy. 
- Post project on Apps-gallery.toolforge.org (WikiMedia's app gallery)
- import Wikipedia? 
