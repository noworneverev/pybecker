from model.becker import Becker
from util.cookie import Cookie
from type.subject import SubjectType

if __name__ == "__main__":
    cookie = Cookie.get_cookie()
    subject_type = SubjectType.Financial
    becker = Becker(cookie, subject_type)
    txt = becker.get_mcsqs()
    print(txt)