from datetime import datetime

def get_user_rank(username, all_users):
    rank = None
    for index, user in enumerate(all_users):
        if username == user["username"]:
            rank = index

    if rank is None:
        rank = "N/A"
    
    return rank+1, len(all_users)


def last_activity(last_logon_time):
    last_sign_in = datetime.strptime(last_logon_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    history = datetime.now() - last_sign_in
    days_ago = str(history.days) + " Days" if history.days > 0 else str(history.seconds / 60) + " Minutes"
    last_sign_in_at_time = datetime.strftime(last_sign_in, "%b %d %Y %I:%M %p")
    last_sign_in_at_date = datetime.strftime(last_sign_in, "%Y-%m-%d")
    print(last_sign_in_at_date)

    return {"datetime": last_sign_in_at_time, "date": last_sign_in_at_date, "days_ago": days_ago}
