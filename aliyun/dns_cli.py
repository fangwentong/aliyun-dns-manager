#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

import sys
import yaml
from dns_ops import AliyunDnsOps


def load_aliyun_conf(path):
    with open(path) as fp:
        return yaml.load(fp, Loader=yaml.FullLoader)


def load_and_update_dns_config(cfg_path):
    aliyun_conf = load_aliyun_conf(cfg_path)
    key_id = aliyun_conf.get("accessKey").get("id")
    key_secret = aliyun_conf.get("accessKey").get("secret")
    ops = AliyunDnsOps(key_id, key_secret)

    for config in aliyun_conf.get("dns"):
        domain = config.get("domain")
        rr = config.get("rr")
        record_type = config.get("type")
        value = config.get("value")
        ttl = config.get("ttl")
        online_records = ops.get_domain_records(domain, rr, record_type)

        # create record if not exists
        while len(online_records) == 0:
            print("try create record [{}] {}.{} -> {}".format(record_type, rr, domain, value))
            print(ops.create_domain_record(domain, rr, record_type, value, ttl))
            online_records = ops.get_domain_records(domain, rr, record_type)

        # update record if value not match
        for record in ops.get_domain_records(domain, rr, record_type):
            record_id = record.get("RecordId")
            while ops.desc_domain_record(record_id).get("Value") != value:
                print("try update record [{}] {}.{} -> {}".format(record_type, rr, domain, value))
                print(ops.modify_domain_record(record_id, rr, record_type, value))
            print("status now [{}] {}.{} -> {}".format(record_type, rr, domain, value))
    print("Done.")


def show_online_config(cfg_path):
    aliyun_conf = load_aliyun_conf(cfg_path)
    key_id = aliyun_conf.get("accessKey").get("id")
    key_secret = aliyun_conf.get("accessKey").get("secret")
    ops = AliyunDnsOps(key_id, key_secret)

    for config in aliyun_conf.get("dns"):
        domain = config.get("domain")
        rr = config.get("rr")
        record_type = config.get("type")
        online_records = ops.get_domain_records(domain, rr, record_type)

        if len(online_records) == 0:
            print("status now [{}] {}.{} -> nil".format(record_type, rr, domain))

        for record in online_records:
            print("status now [{}] {}.{} -> {}".format(record_type, rr, domain, record.get('Value')))

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
    cfg_path = params[1]

    if command == 'update':
        load_and_update_dns_config(cfg_path)
    elif command == 'status':
        show_online_config(cfg_path)
    else:
        print("unknown command", command)


if __name__ == '__main__':
    main()
