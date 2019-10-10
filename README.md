# anka
AWS Cloudformation Helpers

# Requirements

## Cloud
* AWS account
* AWS access key
* AWS secret access key

## Operating System
Ubuntu:
* aws-cli
* bash
* python-3

# How to run this report on daily basis?

Add the following line to crontab

```
# m h  dom mon dow   command
11 11 * * 1-5 /opt/code/anka-your-org/daily-report.sh >> ~/logs/daily-report.log
```
# Next features
* Docker container (aws-cli, reports to S3 bucket)
