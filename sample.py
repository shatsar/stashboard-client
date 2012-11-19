from stashboard_http_check import StashboardHttpCheck

v = StashboardHttpCheck("mashape.com")
v.check()

v = StashboardHttpCheck("www.mashape.com")
v.check()