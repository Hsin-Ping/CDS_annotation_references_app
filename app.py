#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 18:06:51 2024

@author: wangxinping
"""

import streamlit as st
import pandas as pd
import config
from lib.utlis_sql import connet_sqlite, get_matched_subjects
from lib.utlis_subj import Subjects, get_subjs_refs_info

st.set_page_config(layout="wide")

row1 = st.columns(1)
row2 = st.columns(1)
row3 = st.columns(1)
row5 = st.columns(1)

if "blastp_df" not in st.session_state:
    st.session_state["blastp_df"] = pd.DataFrame()

if "default_option" not in st.session_state:
    st.session_state["default_option"]  = []
    
if "obj" not in st.session_state:
    st.session_state["obj"] = None
    
if "linksetdbs" not in st.session_state:
    st.session_state["linksetdbs"] = []
    
if "link_db" not in st.session_state:
    st.session_state["link_db"] = None    
    
def run():
    
    conn = connet_sqlite(config.path_sql)
    
    with row1[0]:
        st.write("# Searching References on NCBI PubMed Databases")
        st.write("### Query Accession Numbers (Using comma to idientify each numbers)")
        acc_inputs = st.text_input("e.g. XP_042756787.1,XP_042756788.1")
        submitted = st.button("Get blastp result")
        if submitted:
            df = get_matched_subjects(conn, acc_inputs, config.param_sheet_name)
            st.session_state["blastp_df"] = df
            default = []
            for query_acc, group in df.groupby("query_acc"):
                top3_subject = group["subject_acc"].iloc[:3].to_list()
                default += top3_subject
                st.session_state["default_option"] = set(default)
            # reset 
            st.session_state["linksetdbs"] = []
            st.session_state["link_db"] = None
            st.session_state["obj"] = None
        
    with row2[0]:
        if not st.session_state["blastp_df"].empty:
            st.dataframe(st.session_state["blastp_df"])
        
    with row3[0]:        
        if not st.session_state["blastp_df"].empty:
            st.write("### Select the subject accession IDs that you want to use to search references")
            options = st.multiselect("You could select multiple subject accession number at a time", set(st.session_state["blastp_df"]["subject_acc"].to_list()), st.session_state["default_option"])
            search = st.button("Search References")
            if search:
                subjects_acc = ",".join(options)
                obj = Subjects(subjects_acc, retmode="json")
                st.session_state["obj"] = obj
                st.session_state["linksetdbs"] = obj.get_linksetdbs()
            
    with row5[0]:
        if st.session_state["linksetdbs"]: 
            row4 = st.columns(len(st.session_state["linksetdbs"]))

            for idx, db in zip(range(len(row4)), st.session_state["linksetdbs"]):
                with row4[idx]: 
                    st.button(db, on_click=get_subjs_refs_info, args=[st.session_state, db])
        
            if not st.session_state["obj"].refs_info.empty:
                st.dataframe(st.session_state["obj"].refs_info, column_config={"PubMed_ID":
                                           st.column_config.LinkColumn("PubMed ID",  display_text="https://pubmed\.ncbi\.nlm\.nih\.gov/([0-9]+)")})
        else:
            if st.session_state["obj"] != None:
                st.write(f"There is no references about {st.session_state['obj'].subject_acc} in NCBI PubMed ")

if __name__ == "__main__":
    config.reload_config()
    run()
    