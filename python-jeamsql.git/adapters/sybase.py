from adapter import Adapter
from multiprocessing import Pool

import re


'''
cPickle.PicklingError: Can't pickle <type 'instancemethod'>:
attribute lookup __builtin__.instancemethod failed

http://stackoverflow.com/a/25161919
'''
import copy_reg
import types

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)



class Sybase(Adapter):

    def __init__(self, *args, **kwargs):

        connection_cmd = "tsql -H%s -p%s -U%s -P%s -o fq" % (
                kwargs.get('server'),
                kwargs.get('port'),
                kwargs.get('user'),
                kwargs.get('password'))

        test_query = "sp_tables"

        # To detect error in output
        pattern = re.compile(r"severity\s+\d+")

        super(Sybase, self).__init__(
                cmd=["tsql"],
                connection_cmd=connection_cmd.split(' '),
                test_query=test_query,
                error_regex=pattern,
                *args,
                **kwargs
        )


    def select(self, query=None, fmt=None):

        super(Sybase, self).select(query=query, fmt=fmt)

        # TODO use sqlparse
        if not query:
            raise SyntaxError("Wrong query %s " % query)

        return self.__runsql__(query, fmt=fmt)


    def execut(self, query):

        super(Sybase, self).execute(query=query)

        # TODO use sqlparse
        if not query:
            raise SyntaxError("Wrong query %s " % query)

        self.__runsql__(query)


    def tables(self, name, fmt=None):

        super(Sybase, self).tables(name=name, fmt=None)

        req = "sp_tables @table_type=\"'TABLE'\""

        if name:
            req = req + (", @table_name='%s'" % name)

        return self.__runsql__(req, fmt=fmt)


    def description(self, table_name=None, fmt=None):

        super(Sybase, self).description(
                table_name=table_name,
                fmt=fmt
                )

        tables = self.tables(name=table_name, fmt="json")
        req = []

        for t in tables:
            req.append((
                "sp_columns @table_name='%s'" % (t['table_name']),
                ))

        p = Pool(1)
        results = p.map(self.__run_parrallel__, req)

        p.close()
        p.join()

        return results

    def __run_parrallel__(self, req):
        self.connect(test=False)
        return self.__runsql__(req, fmt="json")
