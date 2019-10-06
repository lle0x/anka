# anka
AWS Cloudformation Helpers

# how to run this report on daily basis?

Add the following line to crontab

```
# m h  dom mon dow   command
11 11 * * 1-5 ~/code/anka-your-org/daily-report.sh >> ~/logs/daily-report.log
```
