#!/usr/bin/env python
# coding=utf-8

import json
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordInfoRequest import DescribeDomainRecordInfoRequest


class AliyunDnsOps:
    def __init__(self, access_key_id, access_key_secret):
        self.clt = client.AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')

    def get_domain_records(self, domain, rr, record_type):
        page_no = 1
        result = []
        while True:
            res = self._get_domain_records_by_page(domain, rr, record_type, page_no)
            result += res.get("DomainRecords").get("Record")
            if AliyunDnsOps.no_more(res):
                break
            page_no = page_no + 1
        return result

    def _get_domain_records_by_page(self, domain, rr, record_type, page_no):
        desc_domain_req = DescribeDomainRecordsRequest()
        desc_domain_req.set_DomainName(domain)
        desc_domain_req.set_accept_format("JSON")
        desc_domain_req.set_PageNumber(page_no)
        if rr is not None:
            desc_domain_req.set_RRKeyWord(rr)
        if record_type is not None:
            desc_domain_req.set_TypeKeyWord(record_type)
        desc_domain_res = self.clt.do_action_with_exception(desc_domain_req)
        return json.loads(desc_domain_res)

    @staticmethod
    def no_more(desc_domain_res):
        total_count = desc_domain_res.get("TotalCount")
        page_number = desc_domain_res.get("PageNumber")
        page_size = desc_domain_res.get("PageSize")
        current_page_size = len(desc_domain_res.get("DomainRecords").get("Record"))
        return total_count <= (page_number - 1) * page_size + current_page_size

    def desc_domain_record(self, record_id):
        desc_record_req = DescribeDomainRecordInfoRequest()
        desc_record_req.set_RecordId(record_id)
        desc_record_req.set_accept_format("JSON")
        return json.loads(self.clt.do_action_with_exception(desc_record_req))

    def modify_domain_record(self, record_id, rr, record_type, value):
        request = UpdateDomainRecordRequest()
        request.set_Value(value)
        request.set_RecordId(record_id)
        request.set_accept_format('JSON')
        request.set_RR(rr)
        request.set_Type(record_type)
        return json.loads(self.clt.do_action_with_exception(request))

    def create_domain_record(self, domain, rr, record_type, value, ttl):
        request = AddDomainRecordRequest()
        if ttl is not None:
            request.set_TTL(ttl)
        request.set_Type(record_type)
        request.set_RR(rr)
        request.set_Value(value)
        request.set_DomainName(domain)
        request.set_accept_format("JSON")
        return json.loads(self.clt.do_action_with_exception(request))
