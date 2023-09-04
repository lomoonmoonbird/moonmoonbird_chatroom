#--*-- coding:utf-8 --*--

import trafaret as T


TRAFARET = T.Dict({
    T.Key('mongodb'):
        T.Dict({
            'database': T.String(),
            'host': T.String(),
            'port': T.Int(),
            'max_pool_size': T.Int(),
        }),

    T.Key('mysql'):
        T.Dict({
            'database': T.String(),
            'host': T.String(),
            'port': T.Int(),
            'user': T.String(),
            'password': T.String(),
        }),
    T.Key('hashid'):
        T.Dict({
            'salt': T.String(),
            'len': T.Int(),
        }),
    T.Key('jwt'):
        T.Dict({
            'salt': T.String(),
            'expire': T.Int(),
        }),
    T.Key('host'): T.IP,
    T.Key('port'): T.Int(),

}
)

