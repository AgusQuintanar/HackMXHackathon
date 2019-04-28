


import imaplib
from email.parser import HeaderParser
M = imaplib.IMAP4_SSL("imap.gmail.com")
user = "hackmx.prueba1@gmail.com"
password = "buttercorp"
M.login(user, password)
(retcode, messages) = M.sort("DATE", 'UTF-8', 'ALL')
news_mail = get_mostnew_email(messages)
for i in news_mail :
    data = M.fetch(i, '(BODY[HEADER])')
    header_data = data[1][0][1]
    parser = HeaderParser()
    msg = parser.parsestr(header_data)
    print(msg['subject'])

def get_mostnew_email(messages):
    """
    Getting in most recent emails using IMAP and Python
    :param messages:
    :return:
    """
    ids = messages[0]  # data is a list.
    id_list = ids.split()  # ids is a space separated string
    #latest_ten_email_id = id_list  # get all
    latest_ten_email_id = id_list[-10:]  # get the latest 10
    keys = map(int, latest_ten_email_id)
    news_keys = sorted(keys, reverse=True)
    str_keys = [str(e) for e in news_keys]
    return  str_keys