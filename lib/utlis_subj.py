#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:17:14 2024

@author: wangxinping
"""
import pandas as pd
import json
import urllib.request

class Download_from_url:
    def __init__(self):
        self.url_root = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        
    def get_d(self, url):
        d = json.loads(urllib.request.urlopen(url).read())
        return d
        
class Subjects(Download_from_url):
    def __init__(self, subjects_acc, retmode="json"):
        super().__init__()
        self.subject_acc = subjects_acc
        self.retmode = retmode
        self.ref_uids = ""
        self.refs_info = pd.DataFrame()
        self.get_uids()
        
    def get_uids(self):
        get_uids_url = f"{self.url_root}elink.fcgi?dbfrom=protein&db=gene&id={self.subject_acc}&retmode={self.retmode}"
        d = super().get_d(get_uids_url)
        self.uids = ",".join(d["linksets"][0]["linksetdbs"][0]['links'])
        
    def get_linksetdbs(self):
        if self.uids:
            get_linksetdbs_url = f"{self.url_root}elink.fcgi?dbfrom=gene&db=pubmed&id={self.uids}&retmode={self.retmode}"
            d = super().get_d(get_linksetdbs_url)
            if "linksetdbs" in d["linksets"][0].keys(): 
                dbs = [db["linkname"] for db in d["linksets"][0]["linksetdbs"]]
            else:
                dbs = None
        return dbs
        
    def get_references_uids(self, link_db):
        if self.uids:
            get_refs_uid_url = f"{self.url_root}elink.fcgi?dbfrom=gene&db=pubmed&linkname={link_db}&id={self.uids}&retmode={self.retmode}"
            d = super().get_d(get_refs_uid_url)
            if "linksetdbs" in d["linksets"][0].keys():
                ref_uids = d["linksets"][0]["linksetdbs"][0]['links']
                self.ref_uids = ",".join(ref_uids)
            else:
                print("no references")
                
    def get_references_info(self, link_db):
        self.get_references_uids(link_db)
        if self.ref_uids:
            get_refs_info_url = f"{self.url_root}esummary.fcgi?db=pubmed&linkname={link_db}&id={self.ref_uids}&format={self.retmode}"
            d = super().get_d(get_refs_info_url)
            ref_uids_list = self.ref_uids.split(",")
            urls = [f"https://pubmed.ncbi.nlm.nih.gov/{uid}" for uid in ref_uids_list]
            titles = [d['result'][uid]['title'] for uid in ref_uids_list]
            pubdate = [d["result"][uid]["pubdate"] for uid in ref_uids_list]
            source = [d["result"][uid]["source"] for uid in ref_uids_list]
            data = {"PubMed_ID":urls, "Title":titles, "PubDate":pubdate, "Source":source}
            self.refs_info = pd.DataFrame(data)
            
def get_subjs_refs_info(obj_dict, link_db):
    obj_dict["link_db"] = link_db
    obj_dict["obj"].get_references_info(obj_dict["link_db"])