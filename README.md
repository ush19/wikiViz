# wikiViz

##  Inspiration 
Inspiration for this project was drawn from [@terrence.png](https://www.tiktok.com/@terrence.png) on TikTok who maps two Wikipedia pages to each other with only the page's content and context. Combined with my interest in network science, I thought it'd be interesting to build a program to build the connections from nodes (Wikipedia pages) and the links which would lead from Wikipedia page A to Wikipedia page B. 

##  Goals
- Calculate the shortest path between two Wikipedia pages, if any. 
- Return degrees of separation between Wikipedia pages if such a path exists.
- 

##  Questions?
Please send me an email to: palakurthisusheel@gmail.com

##  Connect with me!
Connect with me on [LinkedIn](https://www.linkedin.com/in/psusheel/)!

##  Future Considerations
- Fix direction of network graph to go specifically from A --> node --> node --> B, instead of A --> node --> node <-- B (currently algorithm works in the latter direction), likely caused by the placement of page search B as the second elemnent in the titles list which causes the algorithm to find all links on that page (in hindsight, not an issue but most likely not the proper way to go about finding separation)
- Further develop network visualization from degrees of separation
- Reduce scope of links by removing links which aren't in the direct Wikipedia article
- Simplify how nodes are combined from searches A and B
- Implement other networkx functions, after review of network science and analysis
