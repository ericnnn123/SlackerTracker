def construct_table_information(users):
    def split_seq(seq, size):
        newseq = list()
        splitsize = 1.0/size*len(seq)
        for i in range(size):
            newseq.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
        return newseq

    if len(users) > 3:
        total = list(range(len(users)))
        quartiles = split_seq(total, 4)
        workers = quartiles[0]
        above_avgs = quartiles[1]
        below_avgs = quartiles[2]
        slackers = quartiles[3]
        for index in range(len(users)):
            if index in workers:
                users[index]["status"] = "success"
            if index in above_avgs:
                users[index]["status"] = "info"
            if index in below_avgs:
                users[index]["status"] = "warning"
            if index in slackers:
                users[index]["status"] = "danger"

    if len(users) == 3:
        if users[0]["total"] - users[1]["total"] > users[1]["total"] - users[2]["total"]:
            users[1]["status"] = "info"
        else:
            users[1]["status"] = "warning"

    if len(users) == 2:
        users[0]["status"] = "success"
        users[-1]["status"] = "danger"

    return users

def construct_worker_and_slacker(gitlab, tracker, all_users):
    hardest_worker = all_users[0]['username']
    hardest_slacker = all_users[-1]['username']
    worker_analytics = tracker.compile_analytics_by_user(hardest_worker)
    slacker_analytics = tracker.compile_analytics_by_user(hardest_slacker)

    worker = {
        "name": hardest_worker,
        "img": gitlab.get_user_by_username(hardest_worker)['avatar_url'],
        "commits": worker_analytics['commits'],
        "total": worker_analytics['total'],
        "additions": worker_analytics['additions'],
        "deletions": worker_analytics['deletions']
    }
    slacker = {
        "name": hardest_slacker,
        "img": gitlab.get_user_by_username(hardest_slacker)['avatar_url'],
        "commits": slacker_analytics['commits'],
        "total": slacker_analytics['total'],
        "additions": slacker_analytics['additions'],
        "deletions": slacker_analytics['deletions']
    }
    return worker, slacker
