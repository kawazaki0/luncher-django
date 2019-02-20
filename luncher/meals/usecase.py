import pendulum


def is_user_able_to_order_meal():
    threshold_time = pendulum.today('UTC').set(hour=11)
    now = pendulum.now('UTC')
    return now <= threshold_time
