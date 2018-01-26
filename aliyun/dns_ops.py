#!/usr/bin/env python
#coding=utf-8

import json
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordInfoRequest import DescribeDomainRecordInfoRequest

class AliyunDnsOps:
    def __init__(self, accessKeyId, accessKeySecret):
        self.clt = client.AcsClient(accessKeyId, accessKeySecret, 'cn-hangzhou')

    def getDomainRecords(self, domain, rr, type):
        pageNo = 1
        result = []
        while True:
            res = self._getDomainRecords(domain, rr, type, pageNo)
            result +=  res.get("DomainRecords").get("Record")
            if (AliyunDnsOps.noMore(res)):
                break
            pageNo = pageNo + 1
        return result

    def _getDomainRecords(self, domain, rr, type, pageNumber):
        descDomainReq = DescribeDomainRecordsRequest()
        descDomainReq.set_DomainName(domain)
        descDomainReq.set_accept_format("JSON")
        descDomainReq.set_PageNumber(pageNumber)
        if rr is not None:
            descDomainReq.set_RRKeyWord(rr)
        if type is not None:
            descDomainReq.set_TypeKeyWord(type)
        descDomainRes = self.clt.do_action_with_exception(descDomainReq)
        return json.loads(descDomainRes)

    @staticmethod
    def noMore(descDomainRes):
        totalCount = descDomainRes.get("TotalCount")
        pageNumber = descDomainRes.get("PageNumber")
        pageSize = descDomainRes.get("PageSize")
        currentPageSize = len(descDomainRes.get("DomainRecords").get("Record"))
        return totalCount <= (pageNumber - 1) * pageSize + currentPageSize

    def descDomainRecord(self, recordId):
        descRecordReq = DescribeDomainRecordInfoRequest()
        descRecordReq.get_UserClientIp
        descRecordReq.set_RecordId(recordId)
        descRecordReq.set_accept_format("JSON")
        return json.loads(self.clt.do_action_with_exception(descRecordReq))

    def modifyDomainRecord(self, recordId, rr, type, value):
        request = UpdateDomainRecordRequest()
        request.set_Value(value)
        request.set_RecordId(recordId)
        request.set_accept_format('JSON')
        request.set_RR(rr)
        request.set_Type(type)
        return json.loads(self.clt.do_action_with_exception(request))

    def createDomainRecord(self, domain, rr, type, value, ttl):
        request = AddDomainRecordRequest()
        if (ttl is not None):
            request.set_TTL(ttl)
        request.set_Type(type)
        request.set_RR(rr)
        request.set_Value(value)
        request.set_DomainName(domain)
        request.set_accept_format("JSON")
        return json.loads(self.clt.do_action_with_exception(request))

