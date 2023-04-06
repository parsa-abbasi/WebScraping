# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem  

class PreprocessPipeline:
    def process_item(self, item, spider):
        item['title'] = " ".join(item['title'].split())
        return item

# A filter will check for the repeated items and it will drop the already processed items
class DuplicatesPipeline(object):  
   def __init__(self):
       self.url_seen = set() 

   def process_item(self, item, spider):
       if item['url'] in self.url_seen:
           raise DropItem("Repeated items found: %s" % item)
       else:
           self.url_seen.add(item['url'])
           return item