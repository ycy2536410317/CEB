from query_representation.query import *

src_path = 'queries/job/all_job'
des_path = '/home/ycy/Desktop/PGDev/postgresql-12.5/job-hint'


def get_sql_name(qrep):
    # get the sql name of the query
    # ex : .../queries/job/all_job/1a.pkl -> 1a.sql
    sql_name = qrep['name']
    # remove dir path
    sql_name = sql_name.split('/')[-1]
    sql_name = sql_name.replace('.pkl', '.sql')
    return sql_name


def load_all_qrep(src_path):
    qrep_list = []
    for filename in os.listdir(src_path):
        if filename.endswith(".pkl"):
            qrep = load_qrep(os.path.join(src_path, filename))
            qrep_list.append(qrep)
    return qrep_list


def construct_rows_hint(qrep, trues):
    # ex : trues[('it', 'j')]= 1000
    #  Rows (it j #1000)

    rows_hint = '/*+'
    for k, v in trues.items():
        if len(k) > 1:
            rows_hint += ' Rows (' + ' '.join(k) + ' #' + str(v) + ') '
    rows_hint += '*/'
    # combine sql
    rows_hint += qrep['sql']
    return rows_hint


# read all pickle files from src_path
qrep_list = load_all_qrep(src_path)

# for all qrep in qrep_list
for qrep in qrep_list:
    ests = get_postgres_cardinalities(qrep)
    trues = get_true_cardinalities(qrep)
    rows_hint = construct_rows_hint(qrep, trues)
    # write to des_path
    sql_file_name = get_sql_name(qrep)
    with open(os.path.join(des_path, sql_file_name), 'w') as f:
        f.write(rows_hint)


# # for getting cardinality estimates of every subplan in the query


# for k,v in ests.items():
#     print("Subplan, joining tables: ", k)
#     subsql = subplan_to_sql(qrep, k)
#     print("Subplan SQL: ", subsql)
#     print("   True cardinality: ", trues[k])
#     print("PostgreSQL estimate: ", v)
#     print("****************")
