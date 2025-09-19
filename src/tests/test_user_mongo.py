from daos.user_dao_mongo import UserDAOMongo
from models.user import User

dao = UserDAOMongo()

def test_user_select():
    user = User(None, 'User Test', 'test@example.com')
    assigned_id = dao.insert(user)
    user_list = dao.select_all()
    assert len(user_list) >= 1

def test_user_insert():
    user = User(None, 'Margaret Hamilton', 'hamilton@example.com')
    assigned_id = dao.insert(user)
    user_list = dao.select_all()
    ids = [str(u.id) for u in user_list]
    assert str(assigned_id) in ids

def test_user_update():
    user = User(None, 'Charles Babbage', 'babage@example.com')
    assigned_id = dao.insert(user)

    corrected_email = 'babbage@example.com'
    user.id = assigned_id
    user.email = corrected_email

    dao.update(user)

    user_list = dao.select_all()
    emails = [u.email for u in user_list]
    assert corrected_email in emails

def test_user_delete():
    user = User(None, 'Douglas Engelbart', 'engelbart@example.com')
    assigned_id = dao.insert(user)
    dao.delete(assigned_id)

    user_list = dao.select_all()
    ids = [str(u.id) for u in user_list]
    assert str(assigned_id) not in ids