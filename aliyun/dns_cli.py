#!/usr/bin/env python
#coding=utf-8

from __future__ import print_function

import sys
import yaml
from dns_ops import AliyunDnsOps


def loadAliyunConf(path):
    with open(path) as fp:
        return yaml.load(fp)


def updateDnsConfig(cfgPath):
    aliyunConf = loadAliyunConf(cfgPath)
    keyId = aliyunConf.get("accessKey").get("id")
    keySecret = aliyunConf.get("accessKey").get("secret")
    ops = AliyunDnsOps(keyId, keySecret)

    for config in aliyunConf.get("dns"):
        domain = config.get("domain")
        rr = config.get("rr")
        type = config.get("type")
        value = config.get("value")
        ttl = config.get("ttl")
        currentRecords = ops.getDomainRecords(domain, rr, type)

        # create record if not exsits
        while len(currentRecords) == 0:
            print("try create record [{}] {}.{} -> {}".format(type, rr, domain, value))
            print(ops.createDomainRecord(domain, rr, type, value, ttl))
            currentRecords = ops.getDomainRecords(domain, rr, type)

        # update record if value not match
        for record in ops.getDomainRecords(domain, rr, type):
            recordId = record.get("RecordId")
            while ops.descDomainRecord(recordId).get("Value") != value:
                print("try update record [{}] {}.{} -> {}".format(type, rr, domain, value))
                print(ops.modifyDomainRecord(recordId, type, value))
            print("status now [{}] {}.{} -> {}".format(type, rr, domain, value))
    print("Done.")

def showCurrentConfig(cfgPath):
    aliyunConf = loadAliyunConf(cfgPath)
    keyId = aliyunConf.get("accessKey").get("id")
    keySecret = aliyunConf.get("accessKey").get("secret")
    ops = AliyunDnsOps(keyId, keySecret)

    for config in aliyunConf.get("dns"):
        domain = config.get("domain")
        rr = config.get("rr")
        type = config.get("type")
        currentRecords = ops.getDomainRecords(domain, rr, type)

        if len(currentRecords) == 0:
            print("status now [{}] {}.{} -> nil".format(type, rr, domain))

        for record in currentRecords:
            print("status now [{}] {}.{} -> {}".format(type, rr, domain, record.get('Value')))

    print("End.")

guide = '''\
Usage:
    aliyun-dns-manager <command> [/path/to/dns/config]

Commands:
    status    show current dns status
    update    load dns config from local, flush local config to aliyun
'''

def main():
    params = sys.argv[1:]

    if len(params) < 2:
        print(guide)
        return

    command = params[0]
    cfgPath = params[1]

    if command == 'update':
        updateDnsConfig(cfgPath)
    elif command == 'status':
        showCurrentConfig(cfgPath)
    else:
        print("unknown command", command)

if __name__ == '__main__':
    main()
