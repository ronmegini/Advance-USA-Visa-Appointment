import requests


def get_free_dates(session,user_id):
    
    FREE_DATES_URL = r"https://ais.usvisa-info.com/he-il/niv/schedule/{}/appointment/days/96.json?appointments[expedite]=false"
    
    session_cookie = {'_yatri_session': session}
    tree_dates_json = requests.get(FREE_DATES_URL.format(user_id), cookies=session_cookie)
    return tree_dates_json


if __name__ == "__main__":
    #s = requests.Session()
    session = ""
    user_id = ""
    free_dates = get_free_dates(session,user_id)