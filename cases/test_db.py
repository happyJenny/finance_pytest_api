from utils.db import count

# from utils.db import login_db

# def test_connect_db():
#     login_db()

def test_db_tables_exist():
    """5 张表都存在"""
    #  SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
    cnt = count("""select count(*) from information_schema.tables where table_schema='public'
    and table_name in ('users','accounts','transactions','login_logs','transfer_contacts' )
    """)
    assert cnt == 5, f"期望 5 张表，实际 {cnt}"  

def test_db_transactions_exist():   
        cnt = count("""
        select count(*) from transactions
        """)  
        assert cnt >0, f"期望 transactions 有数据 ，实际 {cnt}"  