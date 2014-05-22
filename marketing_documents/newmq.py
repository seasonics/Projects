from DBConnection import MysqlConnecttion
import json

class Newmq:
    def updatewithids(self):
        local_sql = MysqlConnecttion("local")
        #booth_sql = MysqlConnecttion("booth")
        query = r"select MQID,MQ_title,MQ_date from magic_quadrants"
        rows = local_sql.excute_with_result(query)
        mqlistt = {}
        mqlistd = {}
        for row in rows:
            new = str(row[1]).replace("'","")
            mqlistt[row[0].strip()] = new
            mqlistd[row[0].strip()] = row[2]
        for x in mqlistt:
            query = r'''UPDATE new_magic_quadrants set mq_title = '%s', mq_date = '%s' WHERE MQID = '%s' ''' %(mqlistt[x], mqlistd[x], x)
            local_sql.excute(query)
    def update_labelid_first(self):
        """
            update the labelid in Magic_Quadrants
            """
        local_sql = MysqlConnecttion("local")
        #booth_sql = MysqlConnecttion("booth")
        label_map = {}#{"word":labelid}
        query = r"select Word, Labelid from labels WHERE Geogr = 0 and Vert = 0 and Mktseg = 0"
        rows = local_sql.excute_with_result(query)
        for row in rows:
            label_map[row[0]] = row[1]
        query = r'''(SELECT mqid, docid, labelid, mq_title_vector_short, removed FROM magic_quadrants)'''
        mq_vector_map = {}#{"mqid":"word vector (short)"}
        label_tmap = {}
        docid_map ={}
        rem_map ={}
        rows = local_sql.excute_with_result(query)
        for row in rows:
            mq_vector_map[row[0]] = row[3]
            docid_map[row[0]] = row[1]
            rem_map[row[0]] = row[4]
            label_map[row[0]] = row[2]
        query = r'''(SELECT title_short, docid FROM doc_deatail_vector)'''
        cool_map ={}
        rows = local_sql.excute_with_result(query)
        for row in rows:
            cool_map[row[1]] = row[0]
        for mq_id in mq_vector_map:
            json_word_set = mq_vector_map[mq_id]
            if json_word_set == None or json_word_set == "":
                json_word_set = "{}"
            word_map = json.loads(json_word_set)
            label_list = []
            for word in word_map:
                if word in label_map:
                    label_list.append(str(label_map[word]))
            json_word_set = cool_map[docid_map[mq_id]]
            if json_word_set == None or json_word_set == "":
                json_word_set = "{}"
            word_map = json.loads(json_word_set)
            for word in word_map:
                if word in label_map:
                    label_list.append(str(label_map[word]))
            label_list = list(set(label_list))
            length = len(label_list)
            if length == 0:
                query = r'''insert into new_magic_quadrants (DocID, MQID,removed)
                    values
                    ('%s', '%s', '%s')
                    '''%(docid_map[mq_id], mq_id,rem_map[mq_id])
                local_sql.excute(query)
                #booth_sql.excute(query)
            if length == 1:
                query = r'''insert into new_magic_quadrants (DocID, MQID, Labelid1,removed)
                    values
                    ('%s', '%s', '%s', '%s')
                    '''%(docid_map[mq_id], mq_id, label_list[0],rem_map[mq_id])
                local_sql.excute(query)
                #booth_sql.excute(query)
            if length == 2:
                query = r'''insert into new_magic_quadrants (DocID, MQID, Labelid1,Labelid2,removed)
                    values
                    ('%s', '%s', '%s', '%s', '%s')
                    '''%(docid_map[mq_id], mq_id, label_list[0],label_list[1],rem_map[mq_id])
                local_sql.excute(query)
                #booth_sql.excute(query)
            if length == 3:
                query = r'''insert into new_magic_quadrants (DocID, MQID, Labelid1,Labelid2,Labelid3,removed)
                    values
                    ('%s', '%s', '%s', '%s', '%s', '%s')
                    '''%(docid_map[mq_id], mq_id, label_list[0],label_list[1],label_list[2],rem_map[mq_id])
                local_sql.excute(query)
                #booth_sql.excute(query)
            if length == 4:
                query = r'''insert into new_magic_quadrants (DocID, MQID, Labelid1,Labelid2,Labelid3,Lableid4,removed)
                    values
                    ('%s', '%s', '%s', '%s', '%s', '%s', '%s')
                    '''%(docid_map[mq_id], mq_id, label_list[0],label_list[1],label_list[2],label_list[3],rem_map[mq_id])
                local_sql.excute(query)
                #booth_sql.excute(query)
            if length == 5:
                query = r'''insert into new_magic_quadrants (DocID, MQID, Labelid1,Labelid2,Labelid3,Lableid4,labelid5,removed)
                    values
                    ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                    '''%(docid_map[mq_id], mq_id, label_list[0],label_list[1],label_list[2],label_list[3],label_list[4],rem_map[mq_id])
                local_sql.excute(query)
                #booth_sql.excute(query)
            if length > 5:
                print "lolz"
                return
    def updatewithdocs(self):
        local_sql = MysqlConnecttion("local")
        #booth_sql = MysqlConnecttion("booth")
        query = r"select DocID,Title from documents"
        rows = local_sql.excute_with_result(query)
        doclistt = {}
        for row in rows:
            new = str(row[1]).replace("'", "")
            doclistt[row[0]] = new
        for x in doclistt:
            query = r'''UPDATE new_magic_quadrants set doc_title = '%s' WHERE DocID = '%s' ''' %(doclistt[x],  x)
            local_sql.excute(query)
    def check_hr(self):
            local_sql = MysqlConnecttion("local")
            #booth_sql = MysqlConnecttion("booth")
            query = r"select MQID from new_magic_quadrants WHERE Labelid1 = '120' and Vert_label = '99'"
            rows = local_sql.excute_with_result(query)
            for row in rows:
                query = r"update new_magic_quadrants set Labelid1 = NULL where MQID = '%s'"%(row)
                local_sql.excute(query)
                #booth_sql.excute(query)

    def update_labelid_geo(self):
        """
            update the labelid in Magic_Quadrants
            """
        local_sql = MysqlConnecttion("local")
        #booth_sql = MysqlConnecttion("booth")
        label_map = {}#{"word":labelid}
        query = r"select Word, Labelid from labels WHERE Geogr = 1 and Vert = 0 and Mktseg = 0"
        rows = local_sql.excute_with_result(query)
        for row in rows:
            label_map[row[0]] = row[1]
        query = r'''(SELECT mqid, docid, labelid, mq_title_vector_short FROM magic_quadrants)'''
        mq_vector_map = {}#{"mqid":"word vector (short)"}
        label_tmap = {}
        docid_map ={}
        rows = local_sql.excute_with_result(query)
        for row in rows:
            mq_vector_map[row[0]] = row[3]
            docid_map[row[0]] = row[1]
            label_map[row[0]] = row[2]
        query = r'''(SELECT title_short, docid FROM doc_deatail_vector)'''
        cool_map ={}
        rows = local_sql.excute_with_result(query)
        for row in rows:
            cool_map[row[1]] = row[0]
        for mq_id in mq_vector_map:
            json_word_set = mq_vector_map[mq_id]
            if json_word_set == None or json_word_set == "":
                json_word_set = "{}"
            word_map = json.loads(json_word_set)
            label_list = []
            for word in word_map:
                if word in label_map:
                    label_list.append(str(label_map[word]))
            json_word_set = cool_map[docid_map[mq_id]]
            if json_word_set == None or json_word_set == "":
                json_word_set = "{}"
            word_map = json.loads(json_word_set)
            for word in word_map:
                if word in label_map:
                    label_list.append(str(label_map[word]))
            label_list = list(set(label_list))
            length = len(label_list)
            labels = ";".join(label_list)
            query = r"update new_magic_quadrants set Geo_label = '%s' where MQID = '%s'"%(labels, mq_id)
            local_sql.excute(query)
            #booth_sql.excute(query)

    def update_labelid_vert(self):
        """
            update the labelid in Magic_Quadrants
            """
        local_sql = MysqlConnecttion("local")
        #booth_sql = MysqlConnecttion("booth")
        label_map = {}#{"word":labelid}
        query = r"select Word, Labelid from labels WHERE Geogr = 0 and Vert = 1 and Mktseg = 0"
        rows = local_sql.excute_with_result(query)
        for row in rows:
            label_map[row[0]] = row[1]
        query = r'''(SELECT mqid, docid, labelid, mq_title_vector_short FROM magic_quadrants)'''
        mq_vector_map = {}#{"mqid":"word vector (short)"}
        label_tmap = {}
        docid_map ={}
        rows = local_sql.excute_with_result(query)
        for row in rows:
            mq_vector_map[row[0]] = row[3]
            docid_map[row[0]] = row[1]
            label_map[row[0]] = row[2]
        query = r'''(SELECT title_short, docid FROM doc_deatail_vector)'''
        cool_map ={}
        rows = local_sql.excute_with_result(query)
        for row in rows:
            cool_map[row[1]] = row[0]
        for mq_id in mq_vector_map:
            json_word_set = mq_vector_map[mq_id]
            if json_word_set == None or json_word_set == "":
                json_word_set = "{}"
            word_map = json.loads(json_word_set)
            label_list = []
            for word in word_map:
                if word in label_map:
                    label_list.append(str(label_map[word]))
            json_word_set = cool_map[docid_map[mq_id]]
            if json_word_set == None or json_word_set == "":
                json_word_set = "{}"
            word_map = json.loads(json_word_set)
            for word in word_map:
                if word in label_map:
                    label_list.append(str(label_map[word]))
            label_list = list(set(label_list))
            length = len(label_list)
            labels = ";".join(label_list)
            query = r"update new_magic_quadrants set Vert_label = '%s' where MQID = '%s'"%(labels, mq_id)
            local_sql.excute(query)
            #booth_sql.excute(query)

    def update_labelid_intext(self):
        """
            update the labelid in Magic_Quadrants
            """
        local_sql = MysqlConnecttion("local")
        #booth_sql = MysqlConnecttion("booth")
        label_map = {}#{"word":labelid}
        query = r"select Word, Labelid from labels WHERE Geogr = 0 and Vert = 0 and Mktseg = 0"
        rows = local_sql.excute_with_result(query)
        for row in rows:
            label_map[row[0]] = row[1]
        query = r'''(SELECT mqid, docid, labelid, mq_title_vector_short FROM magic_quadrants)'''
        mq_vector_map = {}#{"mqid":"word vector (short)"}
        label_tmap = {}
        docid_map ={}
        rows = local_sql.excute_with_result(query)
        for row in rows:
            mq_vector_map[row[0]] = row[3]
            docid_map[row[0]] = row[1]
            label_map[row[0]] = row[2]
        query = r'''(SELECT first_short,what_short,market_short, docid FROM doc_deatail_vector)'''
        first_map ={}
        what_map = {}
        market_map = {}
        rows = local_sql.excute_with_result(query)
        for row in rows:
            first_map[row[3]] = row[0]
            what_map[row[3]] = row[1]
            market_map[row[3]] = row[2]
        for mq_id in mq_vector_map:
            label_list =[]
            json_word_set = first_map[docid_map[mq_id]]
            if json_word_set == None or json_word_set == "":
                json_word_set = "{}"
            word_map = json.loads(json_word_set)
            for word in word_map:
                if word in label_map:
                    label_list.append(str(label_map[word]))
            json_word_set = what_map[docid_map[mq_id]]
            if json_word_set == None or json_word_set == "":
                json_word_set = "{}"
            word_map = json.loads(json_word_set)
            for word in word_map:
                if word in label_map:
                    label_list.append(str(label_map[word]))
            json_word_set = market_map[docid_map[mq_id]]
            if json_word_set == None or json_word_set == "":
                json_word_set = "{}"
            word_map = json.loads(json_word_set)
            for word in word_map:
                if word in label_map:
                    label_list.append(str(label_map[word]))

            label_list = list(set(label_list))
            labels = ";".join(label_list)
            query = r"update new_magic_quadrants set Labelid_intext = '%s' where MQID = '%s'"%(labels, mq_id)
            local_sql.excute(query)
           # booth_sql.excute(query)

    def update_labelid_mkt(self):
        """
            update the labelid in Magic_Quadrants
            """
        local_sql = MysqlConnecttion("local")
        #booth_sql = MysqlConnecttion("booth")
        label_map = {}#{"word":labelid}
        query = r"select Word, Labelid from labels WHERE Geogr = 0 and Vert = 0 and Mktseg = 1"
        rows = local_sql.excute_with_result(query)
        for row in rows:
            label_map[row[0]] = row[1]
        query = r'''(SELECT mqid, docid, labelid, mq_title_vector_short FROM magic_quadrants)'''
        mq_vector_map = {}#{"mqid":"word vector (short)"}
        label_tmap = {}
        docid_map ={}
        rows = local_sql.excute_with_result(query)
        for row in rows:
            mq_vector_map[row[0]] = row[3]
            docid_map[row[0]] = row[1]
            label_map[row[0]] = row[2]
        query = r'''(SELECT title_short, docid FROM doc_deatail_vector)'''
        cool_map ={}
        rows = local_sql.excute_with_result(query)
        for row in rows:
            cool_map[row[1]] = row[0]
        for mq_id in mq_vector_map:
            json_word_set = mq_vector_map[mq_id]
            if json_word_set == None or json_word_set == "":
                json_word_set = "{}"
            word_map = json.loads(json_word_set)
            label_list = []
            for word in word_map:
                if word in label_map:
                    label_list.append(str(label_map[word]))
            json_word_set = cool_map[docid_map[mq_id]]
            if json_word_set == None or json_word_set == "":
                json_word_set = "{}"
            word_map = json.loads(json_word_set)
            for word in word_map:
                if word in label_map:
                    label_list.append(str(label_map[word]))
            label_list = list(set(label_list))
            length = len(label_list)
            labels = ";".join(label_list)
            query = r"update new_magic_quadrants set Mkt_label = '%s' where MQID = '%s'"%(labels, mq_id)
            local_sql.excute(query)
            #booth_sql.excute(query)
    def updatechanges(self):
        local_sql = MysqlConnecttion("local")
        #booth_sql = MysqlConnecttion("booth")
        query = r"select MQID,Labelid1,Labelid2,Labelid3,Labelid4,Labelid5 from new_magic_quadrants"
        rows = local_sql.excute_with_result(query)
        newll = {}
        for row in rows:
            if row[1] == None:
                newll[row[0]] =""
            elif row[2] == None:
                newll[row[0]] = row[1]
            elif row[3] == None:
                newll[row[0]] = row[1] + ";" + row[2]
            else:
                newll[row[0]] = row[1] + ";" + row[2] + ";" + row[3]
        query = r"select MQID,Labelid from magic_quadrants"
        rows = local_sql.excute_with_result(query)
        oldll = {}
        for row in rows:
            oldll[row[0]] = row[1]
        for x in oldll:
            query = r'''insert into changes (MQID, old, new)
                    values
                    ('%s', '%s', '%s')
                    '''%(x, oldll[x], newll[x])
            local_sql.excute(query)
    def nolabels(self):
        local_sql = MysqlConnecttion("local")
        #booth_sql = MysqlConnecttion("booth")
        query = r"select MQID from new_magic_quadrants where Labelid1 IS NULL "
        rows = local_sql.excute_with_result(query)
        for row in rows:
            query = r'''insert into no_labels (MQID)
                    values
                    ('%s')
                    '''%(row[0])
            local_sql.excute(query)
    def removed(self):
        local_sql = MysqlConnecttion("local")
        #booth_sql = MysqlConnecttion("booth")
        query = r"select MQID,DocID,removed from new_magic_quadrants"
        rows = local_sql.excute_with_result(query)
        mq_id_to_docid = {}
        docid_to_rem = {}
        for row in rows:
            docid_to_rem[row[1]] = 0
        for row in rows:
            docid_to_rem[row[1]] = docid_to_rem[row[1]] + row[2]
            mq_id_to_docid[row[0]] = row[1]
        docl = mq_id_to_docid.values()
        test = set([x for x in docl if docl.count(x) > 1])
        query = r"select docid from doc_deatail_vector where title_short = ''"
        rows = local_sql.excute_with_result(query)
        empty = []
        for row in rows:
            empty.append(row[0])
        fin = set(test)
        for x in test:
            if x in empty:
                fin.remove(x)
        for x in fin:
            if docid_to_rem[x] >= 1:
                print x
            

            
a = Newmq()
#a.update_labelid_first()
#a.updatewithdocs()
#a.updatewithids()
a.update_labelid_geo()
a.update_labelid_vert()
a.update_labelid_mkt()
a.update_labelid_intext()
a.check_hr()

            
            
