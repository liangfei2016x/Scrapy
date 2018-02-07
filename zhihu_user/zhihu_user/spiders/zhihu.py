# -*- coding: utf-8 -*-
import scrapy
import json
import time
from zhihu_user.items import ZhihuUserItem
from scrapy import spider,Request

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # 一个用户的user_taken
    user_name = "excited-vczh"
    user_url = "https://www.zhihu.com/api/v4/members/{user}?include={include}"
    user_query = "locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count," \
                 "following_count,cover_url,following_topic_count,following_question_count,following_favlists_count," \
                 "following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count," \
                 "columns_count,commercial_question_count,favorite_count,favorited_count,logs_count," \
                 "marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active," \
                 "is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name," \
                 "show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count," \
                 "vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description," \
                 "hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage," \
                 "badge[?(type=best_answerer)].topics"
    # 他关注的人的url
    follow_url = "https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}"
    # 关注他的人url
    followers_url = "https://www.zhihu.com/api/v4/members/{user}/followers?" \
                    "include={include}&offset={offset}&limit={limit}"
    user_list_query = "data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following," \
                      "badge[?(type=best_answerer)].topics"

    def start_requests(self):
        yield Request(url=self.user_url.format(user=self.user_name, include=self.user_query), callback=self.parse_user)

    def parse_user(self, response):
        result = json.loads(response.text)
        print(result)
        item = ZhihuUserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

        yield Request(url=self.follow_url.format(user=item.get("url_token"), include=self.user_list_query,
                                                 offset=0, limit=20), callback=self.parse_follows)
        yield Request(url=self.followers_url.format(user=item.get("url_token"), include=self.user_list_query,
                                                    offset=0, limit=20), callback=self.parse_followers)
    # 关注的人
    def parse_follows(self, response):
        results = json.loads(response.text)
        if "data" in results.keys():
            for result in results.get("data"):
                yield Request(url=self.user_url.format(user=result.get("url_token"), include=self.user_query),
                              callback=self.parse_user)

        if results["paging"]["is_end"] == False:
            next_page = results["paging"]["next"]
            yield Request(url=next_page, callback=self.parse_follows)

    # 关注user的人
    def parse_followers(self, response):
        results = json.loads(response.text)
        if "data" in results.keys():
            for result in results.get("data"):
                yield Request(url=self.user_url.format(user=result.get("url_token"), include=self.user_query),
                              callback=self.parse_user)

        if results["paging"]["is_end"] == False:
            next_page = results["paging"]["next"]
            yield Request(url=next_page, callback=self.parse_followers)


