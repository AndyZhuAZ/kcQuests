import json
import os
import re

import requests
import wikitextparser as wtp

from src.kcwiki.helper import filter_text
from src.kcwiki.quest import Quest
from src.kcwiki.constants import BEFORE_PARSE_FILTERS, URL_LIST, SLOT_ITEM_URL, HEADERS


class Quests:
    output = os.path.dirname(os.path.dirname(__file__))
    files = {}
    quests = []
    slot_items = {}

    def __init__(self):
        self.quest_map = None
        self.session = requests.Session()
        self.session.headers = HEADERS

    def query_solt_items(self):
        result = self.session.get(SLOT_ITEM_URL)
        with open(os.path.join(self.output, 'equip.json'), 'w') as f:
            f.write(result.text)
        items = json.loads(result.text)
        for item in items:
            self.slot_items[item["id"]] = item["chinese_name"] if item["chinese_name"] is not None else item["name"]

    def load_solt_items(self):
        with open(os.path.join(self.output, 'equip.json')) as f:
            result = f.read()
            items = json.loads(result)
            for item in items:
                self.slot_items[item["id"]] = item["chinese_name"] if item["chinese_name"] is not None else item["name"]

    def set_output(self, path):
        self.output = path

    def query_raw_text(self):
        for index, url in enumerate(URL_LIST):
            result = self.session.get(url)
            self.files[index] = []
            self.save_raw_files(result.text, index)

    def save_raw_files(self, text, index):
        # text = filter_text(text, FILTERS)
        pages = text.split('页首}}\n')
        for page_index, page in enumerate(pages[1:]):
            output_path = os.path.join(self.output, 'temp')
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            with open(os.path.join(output_path, '{}-{}.txt'.format(index, page_index)), 'w',
                      encoding='utf-8') as f:
                content = page.split('{{页尾')[0]
                f.write(content)
                self.files[index].append(content)

    def json(self):
        return [item.to_json() for item in self.quests]

    def save_json_kcq(self):
        for key in self.quest_map.keys():
            d = {}
            if key == 0:
                for quest in self.quests:
                    d.update(quest.to_dict_without_id())
                filename = os.path.join(self.output, 'quests-scn.json')
            else:
                for quest in self.quest_map[key]:
                    d.update(quest.to_dict_without_id())
                filename = os.path.join(self.output, 'quests-scn-new.json')

            with open(filename, 'w', encoding='utf-8') as f:
                content = json.dumps(d, sort_keys=True, ensure_ascii=False, indent=2)
                f.write(content)

    def parse(self):
        self.quest_map = {}
        for key in self.files.keys():
            self.quest_map[key] = []
            _quests = []
            for index, item in enumerate(self.files[key]):
                item = filter_text(item, BEFORE_PARSE_FILTERS)
                parsed = wtp.parse(item)
                for template in parsed.templates:
                    if template.name.strip() == '任务表':
                        if not template.comments:
                            continue
                        if not template.comments[0]:
                            continue
                        if template.comments[0].contents.strip() == '':
                            continue

                        quest = Quest.from_wt_template(template=template, items=self.slot_items)
                        _quests.append(quest)
            self.quest_map[key] = _quests
            self.quests.extend(_quests)
        return self.quest_map

