#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 01:46:14 2022

@author: susheel
"""

#import necessary modules for package
import wikipediaapi
#import pandas as pd
import networkx as nx
import copy
#from datetime import date
#from itertools import zip_longest
from datetime import datetime
import streamlit as st

st.title('What connects two Wikipedia pages?")

with st.form(key = 'my_form_to_submit'):
    #taking the more straightforward route, user supplies program with 2 wikipedia links themselves
    #search_node_a = input("enter first wikipedia page name: ")
    #search_node_b = input("enter second wikipedia page name: ")
    
    #modified above string inputs for streamlit app
    search_node_a = st.text_input("enter first wikipedia page name: ", "")
    search_node_b = st.text_input("enter second wikipedia page name: ", "")

    submit_button = st.form_submit_button(label = 'Submit')


if submit_button: 
    #get Wikipedia page for the search nodes a, b
    wiki_wiki = wikipediaapi.Wikipedia('en')
    
    page_a = wiki_wiki.page(search_node_a)
    page_b = wiki_wiki.page(search_node_b)
    
    
    #f'ns used to get links from Wikipedia pages and clean page links list to remove Wikipedia attributes 
    def return_links(page, list_n):
        list_n.clear()
        links = page.links
        for title in sorted(links.keys()):
            list_n.append(title)
                
    def clean_links(list_node):
        for item in list_node.copy():
            if ((item in ('Wayback Machine', 'Specials (Unicode block)')) or (item.endswith(('(disambiguation)', '(identifier)'))) or (item.startswith(('List of ', 'Category:', 'File:', 'Help:', 'Talk:', 'Template:', 'Wikipedia:', 'Template talk:', 'Portal:', 'Wiki')))):
                list_node.remove(item)
                
                
    list_node_a = []
    list_node_b = []
    
    return_links(page_a, list_node_a)
    return_links(page_b, list_node_b)
    
    clean_links(list_node_a)
    clean_links(list_node_b)
    
    
    #add page title to graph dict as key and nodes as values
    #form the network from the graph dict 
    graph = {}
    
    graph[(page_a.title)] = list_node_a
    graph[(page_b.title)] = list_node_b
    
    G = nx.to_networkx_graph(graph)
    
    
    now = datetime.now()
    
    page_links = []
    
    error = ""
    shortest_path_list = ""
    
    combined_a_b = list_node_a + list_node_b
    
    
    titles = combined_a_b
    
    for t in titles:
        page = wiki_wiki.page(t)
        return_links(page, page_links)
        clean_links(page_links)
        
        graph[(page.title)] = copy.deepcopy(page_links)
        
        for p in page_links:
            if p not in titles:
                titles.append(p)
            else:
                break;
            break;
                
        page_links.clear();
        del page; 
        
        try:
            G = nx.to_networkx_graph(graph)
            nx.shortest_path(G, page_a.title, page_b.title)
        except nx.NetworkXNoPath:
            if t == titles[-1]: 
                error = "No path found between %s and %s" % (page_a.title, page_b.title)
                break;
            else:
                #print(t)
                continue;
        else:
            shortest_path_list = nx.shortest_path(G, page_a.title, page_b.title)
            break;
    
        if error != "":
            break;
    
    if error == "":
        output = ("There are " + str(len(shortest_path_list) - 1) + " degrees of separation between " + page_a.title + " and " + page_b.title + "\n\n" + str(shortest_path_list))
    else:
        output = error
        
    #print(output)
    st.write(output) 
   
    log = open("app_run_logs.txt", "a")
    log.write(output + "\n")
    log.write("Run: " + str(now) + "\n\n")
    log.close()
