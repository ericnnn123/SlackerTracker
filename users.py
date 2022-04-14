

def get_user_rank(username, all_users):
    rank = None
    for index, user in enumerate(all_users):
        if username == user["username"]:
            rank = index

    if rank is None:
        rank = "N/A"
    
    return rank+1, len(all_users)


