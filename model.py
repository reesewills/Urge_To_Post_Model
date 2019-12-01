from User import User
import numpy as np
import random

def action_wp(p):
    """ Perform action with probability (wp) p
    :param p (int): prob
    """
    return np.random.choice([True, False], p=[p, 1-p])

def compute_avg_utp(users):
    t = 0
    for u in users:
        t += u.urge_to_post
    return t / len(users)

def compute_avg_ute(users):
    t = 0
    for u in users:
        t += u.urge_to_engage
    return t / len(users)

def model_posting(users):
    """ Model all posts that will happen in one day
    :param users (List[User]):
    """
    posts_today = []
    for u in users:
        # will_post = np.random.choice([True, False], p=[u.urge_to_post, 1-u.urge_to_post])
        if action_wp(u.urge_to_post):
            if u.add_post():
                posts_today.append(u.posts[-1])
    return posts_today

def model_engagement(users, posts_today):
    """ Model all engagements that will happen in one day
    :param users (List[User]):
    """
    for u in users:
        for post in posts_today:
            if u is post.owner:
                continue
            # will_engage = np.random.choice([True, False], p=[u.urge_to_engage, 1-u.urge_to_engage])
            if action_wp(u.urge_to_engage):
                post.engagement += 1
                u.add_point()

def update_utp_ute(users, k):
    """ Update each user's urge-to-post and urge-to-engage based off new posts
        and engagements today
    :param users (List[User]):
    """
    for u in users:
        # calculate utp
        if len(u.posts):
            weights = range(1, len(u.posts)+1)
            average_engagement = sum(x * y for x, y in zip(u.posts, weights)) / sum(weights)
            new_utp = 1 - np.exp(-k * average_engagement)
            u.urge_to_post = (u.urge_to_post / 2.0) + (new_utp / 2.0)

        # calculate ute
        diff = len(u.posts) - u.post_cost
        f =  np.exp(k * (-u.urge_to_post * diff))
        u.urge_to_engage = f / (1 + f)
        # print(u.urge_to_post, u.urge_to_engage)

def run_day(users):
    """ Simulate one day
    :param users (List[User]):
    """
    k = 1
    posts_today = model_posting(users)
    model_engagement(users, posts_today)
    update_utp_ute(users, k)

def run_exp(cost_model_users, no_cost_model_users, days):
    """
    :param cost_model_users (List[User]): users in our cost model
    :param no_cost_model_users (List[User]): users in typical no cost model
    :param days (int): number of days to run experiment
    """
    while 0 < days:
        print(f'DAY {days} ===============================')
        run_day(cost_model_users)
        run_day(no_cost_model_users)
        print(f'COST UTP: {compute_avg_utp(cost_model_users)}    COST UTE: {compute_avg_ute(cost_model_users)}')
        print(f'NO_COST UTP: {compute_avg_utp(no_cost_model_users)}     NO_COST UTE: {compute_avg_ute(no_cost_model_users)}')
        days -= 1

def generate_users(n):
    cost_model_users = []
    no_cost_model_users = []
    for i in range(n):
        utp, ute = np.random.uniform(), np.random.uniform()
        cost_model_users.append(User(utp, ute))
        no_cost_model_users.append(User(utp, ute, 0))
    return (cost_model_users, no_cost_model_users)

n, days = 50, 50
cost_model_users, no_cost_model_users = generate_users(n)
run_exp(cost_model_users, no_cost_model_users, days)
