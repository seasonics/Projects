from DBConnection import MysqlConnecttion
import difflib

class Authors:
    def author_list(self):
        local_sql = MysqlConnecttion("local")
        #booth_sql = MysqlConnecttion("booth")
        query = r"select Author from documents where MagicQuadrant = 1"
        rows = local_sql.excute_with_result(query)
        authors = []
        slist = []
        alist = set()
        for row in rows:
            row = str(row[0]).rstrip()
            slist = row.split(", ")
            for x in slist:
                authors.append(x)
        query = r"select author from authors"
        rows = local_sql.excute_with_result(query)
        for row in rows:
            row = str(row[0])
            authors.append(row)
        authors = list(set(authors))
        for x in authors:
            s = unicode(x, errors = 'ignore')
            alist.add(s)
        return alist
    def list_to_dic(self, list_a):
        adic = {}
        check = 0
        for x in list_a:
            check = 0
            if x in adic:
                continue
            else:
                for key in adic:
                    s = difflib.SequenceMatcher(None, x, key)
                    if (s.ratio() > .8):
                        adic[key] = adic[key]  + x + ', '
                        check = 1
                        break
                if check == 0:
                    adic[x] = ''
        for key in adic:
            if adic[key] == '':
                continue
            else:
                adic[key] = adic[key][:-2]
        return adic
    def add_ids(self,adic):
        local_sql = MysqlConnecttion("local")
        author_string = ''
        i = 1;
        for key in adic:
            if adic[key] == '':
                author_string = key
            else:
                author_string = key +  ', ' + adic[key]
            query = r'''insert into author_to_id (author, id)
                        values
                        ('%s', '%s')
                        '''%(author_string, i)
            local_sql.excute_with_result(query)
            i = i+1
    def add_ids_to_authors(self):
        local_sql = MysqlConnecttion("local")
        query = r"select author, id from author_to_id"
        rows = local_sql.excute_with_result(query)
        adic = {}
        for row in rows:
            astring = row[0].split(', ')
            for x in astring:
                adic[x] = row[1]
        query = r"select Author from documents where MagicQuadrant = '1' "
        rows = local_sql.excute_with_result(query)
        for row in rows:
            i_string = ''
            astring = row[0].split(', ')
            for x in astring:
                i_string = i_string + str(adic[x.rstrip()]) + ', '
            if (len(astring) > 0):
                i_string = i_string[:-2]
            query = r"UPDATE documents SET author_id = '%s' WHERE Author = '%s'"%(i_string,row[0])
            local_sql.excute_with_result(query)
            
            
        
alist = ()
a = Authors()
##alist = a.author_list()
##adic = a.list_to_dic(alist)
a.add_ids_to_authors()

        
            
            
