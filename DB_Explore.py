import os
import sqlite3
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import schema

con = sqlite3.connect("PHX_AZ.db")
con.text_factory = str
cur = con.cursor()