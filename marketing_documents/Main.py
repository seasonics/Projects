from __future__ import division # for division
import sys
import codecs
import re
import time
import datetime
import os
import binascii
import MySQLdb as mdb
import string
import nltk
import cPickle as pickle
from nltk.stem.porter import PorterStemmer
import nltk.corpus

import simplejson as json
from Log import Log
from DBConnection import MysqlConnecttion

#main
if __name__ == "__main__":
    from time import clock
    start=clock()
    #from booth.capital_2_words import Process
    #cw = Process()
    #cw.do_xlsx()
    #from get_topic_with_pairs import Topic
    #topic = Topic()
    ##type_list = ["title", "title_first"]
    #type_list = ["title_first"]
    #for type in type_list:
    #    topic.extract(type)

    #from booth.get_mq_title_vector import MQTopic
    #mq_topic = MQTopic()
    #mq_topic.extract()

    # from booth.get_topic import Topic
    # t = Topic()
    ##t.updateTopic()
    # t.extract("title")
    # t.unique_mq()
    ###t.get_mq_matrix()
    ##t.get_content_matrix()

    #from booth.doc_freq_with_pair import DocFreq
    #df = DocFreq()
    #type_list = ["title"]
    #for type in type_list:
    #    df.compute_mq(type)
    #    df.compute_doc(type)

    # from booth.reget_topic_with_pairs import Reprocess
    # re = Reprocess()
    ##re.compute_doc("title")
    # re.compute_mq()
    # re.compute_doc_title()
    #t.unique_mq()

    #from booth.cosine import DocCos
    #dcos = DocCos()
    #type_list = ["topic_title_ad"]
    #for type in type_list:
    #    dcos.compute(type)

    #from booth.get_mq_detail import Process
    #p = Process()
    #p.do_xlsx();


    #from booth.FirmConnection import FirmConnection
    #fc =  FirmConnection()
    #fc.do()



    #from booth.doc_network import NetWork
    #n = NetWork()
    #n.get_similarity_edge()
    #n.get_counts_edge()
    #n.get_nodes()
    #n.test()

    #from GetCrime import GetCrimeData
    #g = GetCrimeData()
    #g.multi_thread_do()

    #from booth.mq_firm import MQ_Firm
    #mf = MQ_Firm()
    #mf.do_xlsx()

    #from booth.MarketDefinition import MarketDefinition
    #md = MarketDefinition()
    #md.extract()
    #md.count()

    #from booth.LabelFirstYear import LabelFirstYear
    #lfy = LabelFirstYear()
    #lfy.do_xlsx()


    # from booth.MQ_network_mod import MQ_network_mod
    # mq_network_mod = MQ_network_mod()
    #mq_network_mod.do_csv()
    #mq_network_mod.do_by_word_csv()
    #mq_network_mod.get_word_list()
    #mq_network_mod.update_word_space()

    from labels import Labels
    l = Labels()
    #l.fill_label_table()
    #l.doc_title_get_word_vector()
    l.doc_title_shorten_word_vector()
    l.mq_title_shorten_word_vector()
    #l.update_super_label()
    #l.update_mq_id()
    #l.update_labelid_first()
    #l.update_labelid_geo()
    #l.update_labelid_vert()
    #l.update_labelid_mkt()
    #l.check_hr()
    #l.update_labelid()
    # l.update_flag_in_mq_table()
    # l.update_numeric_docid()
    # l.remove_invalid_symbols()
    # l.fill_mq_with_no_mq_doc()
    #l.doc_title_labels()
    #l.text_labels()
    # l.repair()
    #from linkscrap import Authors
    #a = Authors()
    #a.fill_author_table()
    
    # from booth.full_text_sim import FullTextSimilarity
    # ft_sim = FullTextSimilarity()
    # ft_sim.compute()



    #from booth.WordCheck import WordCheck
    #wc = WordCheck()
    #wc.do_xlsx()
    finish=clock()
    print "%.2f s"%((finish-start))
    print "done"
