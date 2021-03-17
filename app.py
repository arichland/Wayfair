_author_ = 'arichland'
import orders
import datetime


# Setup date for API records
dtime = datetime.datetime
date = datetime.date
delta = datetime.timedelta

update_date = date.today() - delta(days=1)
#update_date = date(2020, 1, 1)

orders.wf_orders(update_date)