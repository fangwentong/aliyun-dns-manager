Aliyun DNS Manager
---

A command line tool to help you manage aliyun dns records

## Install

```
pip install https://github.com/fangwentong/aliyun-dns-manager/archive/master.zip
```

## Usage

Write your config file (refer to [aliyun_sample.yml](conf/aliyun_sample.yml)), pass the file path to the command.


```
$ aliyun-dns-manager

Usage:
    aliyun-dns-manager <command> [/path/to/dns/config]

Commands:
    status    show current dns status
    update    load dns config from local, flush local config to aliyun


$ aliyun-dns-manager status aliyun_sample.yml

status now [A] @.example.com -> 93.184.216.34
status now [A] www.example.com -> 93.184.216.34
status now [A] plus.example.com -> nil
```
