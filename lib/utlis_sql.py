#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:26:42 2024

@author: wangxinping
"""
import sqlite3
import pandas as pd


def connet_sqlite(sqlite_name):
    conn = sqlite3.connect(sqlite_name)
    return conn

def get_matched_subjects(conn, acc_inputs, sheet_name):
    cols = "query_acc, subject_acc, subject_title, identity, evalue, bit_score, subject_tax_ids"
    
    if not acc_inputs.find(",") == -1:
        query_list = tuple(acc_inputs.replace(" ","").split(","))
        cmd = f"SELECT {cols} FROM {sheet_name} where query_acc in {query_list}"
    else:
        cmd = f"SELECT {cols} FROM {sheet_name} where query_acc = '{acc_inputs.strip(' ')}'"
    cur = conn.cursor()
    cur.execute(cmd)
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=cols.split(", "))
    return df