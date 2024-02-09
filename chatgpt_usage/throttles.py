from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class UsageAnonRateThrottle(AnonRateThrottle):
    THROTTLE_RATES = {"anon": "1/10min"}

class UsageUserRateThrottle(UserRateThrottle):
    THROTTLE_RATES = {"user": "1/10min"}