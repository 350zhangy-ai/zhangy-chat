#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI 助手核心模块 - 智能回复（R3 优化版）
啥都能聊，实用为主
"""

import random
from typing import Optional, List, Dict
from datetime import datetime


class Assistant:
    """AI 助手类"""

    def __init__(self, config: Optional[Dict] = None, 
                 mood_manager=None, preset_manager=None):
        self.config = config or {}
        self.name = self.config.get('personality', {}).get('name', 'zhangy')
        self.style = self.config.get('personality', {}).get('说话风格', [])
        
        # 心情管理器
        self.mood_manager = mood_manager
        # 预设管理器
        self.preset_manager = preset_manager

        # 实用回复库 - 覆盖生活各方面
        self.practical_responses = {
            # 饮食类
            "饿": {
                "keywords": ["饿", "吃饭", "吃东西", "肚子", "食堂", "外卖", "做饭"],
                "response": """## 🍚 吃饭建议

**快速解决**:
- 点外卖：美团/饿了么，30 分钟送到
- 楼下快餐：10-15 元搞定
- 泡面 + 蛋：5 分钟，加根火腿更香

**健康选择**:
- 自己做饭：少油少盐，营养均衡
- 沙拉 + 鸡胸：减脂期首选
- 杂粮饭 + 蔬菜：饱腹感强

**不知道吃啥？试试**:
1. 打开外卖软件看推荐
2. 想想昨天/前天吃了啥，换换口味
3. 问问朋友/同事吃的啥

想好吃啥了吗？没的话我可以帮你推荐～"""
            },
            # 视频类
            "视频": {
                "keywords": ["视频", "剪辑", "拍摄", "抖音", "B 站"],
                "response": """## 📹 视频制作建议

**新手入门**:
1. 用手机拍就行，不用买相机
2. 剪映 APP 足够用，免费还简单
3. 先模仿热门视频，慢慢找感觉

**内容方向**:
- 记录日常生活
- 分享专业技能
- 测评好物
- 教学教程

**变现方式**:
- 平台分成（B 站/西瓜视频）
- 接广告
- 带货佣金
- 知识付费

想做啥类型的视频？说说我帮你出出主意～"""
            },
            # 学习类
            "学习": {
                "keywords": ["学习", "考试", "复习", "备考", "考研", "考证"],
                "response": """## 📚 学习建议

**高效方法**:
- 番茄钟：25 分钟专注 +5 分钟休息
- 费曼技巧：尝试给别人讲懂
- 错题本：记录易错点，定期复习

**时间规划**:
- 早上：背单词/记忆类
- 下午：做题/练习类
- 晚上：总结/复盘

**备考建议**:
1. 先做一套真题，了解难度
2. 制定复习计划，倒推时间节点
3. 重点突破，不要平均用力

在准备啥考试？我可以帮你规划规划～"""
            },
            # 工作类
            "工作": {
                "keywords": ["工作", "上班", "职场", "老板", "同事", "加班", "辞职"],
                "response": """## 💼 工作建议

**职场生存**:
- 少说话多做事，尤其是新人
- 和同事保持距离，别太亲近也别太疏远
- 老板画饼听听就好，实际利益最重要

**提升效率**:
- 早上处理最难的任务
- 批量回复消息，别随时被打断
- 下班前整理明天待办

**关于跳槽**:
- 干得不开心就先骑驴找马
- 拿到 offer 再提离职
- 涨薪最快的方式是跳槽

工作上遇到啥事了？可以跟我吐槽吐槽～"""
            },
            # 情感类
            "喜欢": {
                "keywords": ["喜欢", "暗恋", "表白", "恋爱", "对象", "单身"],
                "response": """## 💕 情感建议

**暗恋阶段**:
- 先当朋友处，多接触多了解
- 观察对方对你有没有特殊对待
- 时机成熟再表白，别太急

**恋爱中**:
- 多沟通，别让猜来猜去
- 给彼此空间，别太黏
- 小矛盾别上纲上线

**单身**:
- 先过好自己，花若盛开蝴蝶自来
- 多参加社交活动，扩大圈子
- 别将就，宁缺毋滥

感情方面遇到啥问题了？说说看～"""
            },
            # 健康类
            "健康": {
                "keywords": ["健康", "运动", "减肥", "健身", "生病", "感冒", "头疼"],
                "response": """## 💚 健康建议

**日常保健**:
- 每天走 6000 步以上
- 少喝奶茶，多喝水
- 11 点前睡觉，别熬夜

**减肥**:
- 管住嘴比迈开腿重要
- 戒掉零食和夜宵
- 高蛋白 + 适量碳水 + 大量蔬菜

**小毛病**:
- 感冒：多喝水，维 C 泡腾片
- 头疼：休息，别硬撑
- 胃不舒服：清淡饮食，按时吃饭

*严重的话一定要去医院*

最近身体哪里不舒服？"""
            },
            # 购物类
            "购物": {
                "keywords": ["购物", "买", "推荐", "好物", "淘宝", "京东"],
                "response": """## 🛒 购物建议

**买前思考**:
1. 真的需要吗？
2. 使用频率会高吗？
3. 有平替吗？

**省钱技巧**:
- 等促销：618、双 11、双 12
- 比价：同款不同平台差价可能很大
- 返利 APP：能省一点是一点

**避坑**:
- 看差评，别看好评
- 注意退换货政策
- 警惕"限时抢购"

想买啥？我帮你参谋参谋～"""
            },
            # 旅行类
            "旅行": {
                "keywords": ["旅行", "旅游", "出去玩", "景点", "酒店", "机票"],
                "response": """## ✈️ 旅行建议

**目的地选择**:
- 预算少：周边城市/省内
- 时间紧：选一个城市深度游
- 想放松：海边/山区度假村

**省钱技巧**:
- 机票：提前 1-2 个月买，周二下午最便宜
- 酒店：多平台对比，看差评
- 门票：学生证/老年证有优惠

**必备物品**:
- 证件：身份证/学生证
- 电子：充电宝、充电器
- 药品：感冒药、肠胃药、创可贴

想去哪玩？我可以帮你做攻略～"""
            },
            # 无聊类
            "无聊": {
                "keywords": ["无聊", "没事干", "闲", "打发时间"],
                "response": """## 🎮 无聊时可以做的事

**宅家**:
- 刷剧/电影：豆瓣高分榜
- 看书：微信读书免费看
- 打游戏：放松一下
- 学做菜：从简单的开始

**出门**:
- 公园散步
- 博物馆/美术馆
- 电影院
- 健身房

**提升自己**:
- 学个技能（PS/剪辑/外语）
- 健身减肥
- 考个证

想干啥类型的？我帮你具体推荐推荐～"""
            },
            # 累类
            "累": {
                "keywords": ["累", "辛苦", "困", "乏", "疲惫"],
                "response": """## 😴 累了就休息休息

**快速恢复**:
- 小睡 20 分钟
- 洗个热水澡
- 听点轻音乐
- 出去走走

**长期调节**:
- 保证睡眠，别熬夜
- 适当运动，出出汗
- 周末彻底放松一天

**心理调节**:
- 别给自己太大压力
- 该躺平的时候就躺平
- 工作不是生活的全部

最近是不是太辛苦了？好好休息休息吧～"""
            }
        }

        # 简单对话
        self.simple_queries = {
            "你叫什么": f"我叫 {self.name}，是你的专属 AI 助手～",
            "你是谁": f"我是 {self.name}，一个本地 AI 助手，可以帮你管理任务、规划目标、聊天解闷～",
            "你好": "你好呀！有什么我可以帮你的吗？",
            "早上好": "早上好！今天也要加油哦～",
            "中午好": "中午好！吃饭了吗？记得休息一下～",
            "晚上好": "晚上好！忙了一天辛苦啦，记得早点休息～",
            "谢谢": "不客气～有其他问题随时找我！",
            "再见": "再见！有需要随时叫我～",
            "在吗": "在的在的～有什么可以帮你的？",
            "帮个忙": "没问题，说吧，什么事？",
            "哈哈": "开心就好～",
            "嗯": "嗯嗯，我在听～",
            "哦": "怎么了？有啥事吗？",
            "啊": "咋了？遇到啥事了？",
        }
        
        # 情绪疏导话术库
        self.emotional_responses = {
            "anxiety": [
                "我理解你现在的感受。焦虑是正常的情绪反应，让我们一起深呼吸，慢慢分析问题。",
                "感到焦虑时，可以试试：1) 深呼吸 5 次 2) 把担忧写下来 3) 专注于当下能做的事",
                "你已经在努力了，这很棒。让我们把大问题拆成小步骤，一步一步来。"
            ],
            "frustrated": [
                "遇到挫折确实让人沮丧。不过你已经走了这么远，不妨休息一下再出发。",
                "挫折是成长的一部分。要不要先暂停一下，做些喜欢的事调整状态？",
                "我理解你的感受。有时候暂时放下问题，反而能找到新的解决思路。"
            ],
            "tired": [
                "辛苦了！适当的休息是为了更好地前进。要不要先放松一下？",
                "疲惫的时候，效率会下降。建议先休息，等状态恢复再继续。",
                "你已经做得很好了。记得照顾好自己，休息也是重要的任务。"
            ],
            "overwhelmed": [
                "事情太多时确实容易感到压力。让我们先列出优先级，一件一件来处理。",
                "深呼吸，你不需要一次性解决所有问题。先找出最重要的那件事。",
                "我理解这种被压得喘不过气的感觉。让我们先暂停，重新规划一下。"
            ]
        }

    def _get_mood_prefix(self) -> str:
        if self.mood_manager:
            return self.mood_manager.get_response_prefix()
        return ""
    
    def _get_mood_suffix(self) -> str:
        if self.mood_manager:
            return self.mood_manager.get_response_suffix()
        return ""
    
    def _apply_mood_style(self, response: str) -> str:
        if not self.mood_manager:
            return response
        
        prefix = self._get_mood_prefix()
        suffix = self._get_mood_suffix()
        
        if self.mood_manager.is_efficiency_mode():
            response = response.split('\n\n---\n')[0]
        
        parts = []
        if prefix:
            parts.append(prefix)
        parts.append(response)
        if suffix:
            parts.append(suffix)
        
        return "\n\n".join(parts)

    def chat(self, query: str) -> str:
        """通用对话 - 优先级：简单对话 > 情绪 > 实用 > 任务 > 默认"""
        
        # 1. 简单对话
        for key, response in self.simple_queries.items():
            if key in query:
                return self._apply_mood_style(response)
        
        # 2. 情绪检测
        emotion = self._detect_emotion(query)
        if emotion:
            return self._apply_mood_style(self._emotional_response(emotion, query))

        # 3. 实用回复（核心功能）
        practical = self._check_practical_query(query)
        if practical:
            return self._apply_mood_style(practical)

        # 4. 任务相关
        if self._is_task_related(query):
            return self._apply_mood_style(self._task_response(query))

        # 5. 内容辅助
        if self._is_content_help(query):
            return self._apply_mood_style(self._content_help(query))

        # 6. 默认回复 - 尝试给出有用信息
        return self._apply_mood_style(self._default_response(query))
    
    def _check_practical_query(self, query: str) -> Optional[str]:
        """检查实用回复库"""
        for category, data in self.practical_responses.items():
            for keyword in data["keywords"]:
                if keyword in query:
                    return data["response"]
        return None

    def _detect_emotion(self, text: str) -> Optional[str]:
        anxiety_words = ['焦虑', '担心', '害怕', '紧张', '不安', '慌']
        frustrated_words = ['沮丧', '挫败', '失望', '灰心', '郁闷', '烦']
        tired_words = ['累', '疲惫', '疲倦', '困', '辛苦', '乏力']
        overwhelmed_words = ['压力大', '喘不过气', '太多事', '应付不来', '崩溃']

        if any(w in text for w in anxiety_words):
            return "anxiety"
        if any(w in text for w in frustrated_words):
            return "frustrated"
        if any(w in text for w in tired_words):
            return "tired"
        if any(w in text for w in overwhelmed_words):
            return "overwhelmed"
        return None

    def _emotional_response(self, emotion: str, query: str) -> str:
        responses = self.emotional_responses.get(emotion, [])
        base = random.choice(responses) if responses else "我理解你的感受，想和我多聊聊吗？"
        
        if self.mood_manager and self.mood_manager.is_empathetic_mode():
            return f"""## {self.name} 想说

{base}

我在这里陪着你，有什么想说的都可以告诉我。
"""
        return f"""## {self.name} 想说

{base}

---
*如果你需要具体建议，可以告诉我更多细节*
"""

    def _is_task_related(self, query: str) -> bool:
        return any(k in query for k in ['任务', '待办', '计划', '安排', '提醒', '目标', '习惯'])

    def _task_response(self, query: str) -> str:
        if self.preset_manager and self.preset_manager.is_focus_mode():
            return """## 任务建议
1. 明确优先级
2. 拆解大任务
3. 设置截止时间
4. 定期复盘

用 `/add` 添加任务，`/review` 生成复盘。
"""
        return """## 任务建议

关于任务管理：
1. 明确优先级：区分重要紧急程度
2. 拆解大任务：分解为小步骤
3. 设置截止时间：合理期限
4. 定期复盘：回顾调整

用 `/add` 添加任务，`/review` 生成复盘～
"""

    def _is_content_help(self, query: str) -> bool:
        return any(k in query for k in ['润色', '修改', '优化', '总结', '摘要', '大纲', '整理'])

    def _content_help(self, query: str) -> str:
        if any(k in query for k in ['润色', '修改', '优化']):
            return "## 内容润色\n\n请提供需要润色的文本，我可以帮你优化表达、调整语气、修正语法、提升逻辑～"
        if any(k in query for k in ['总结', '摘要']):
            return "## 内容摘要\n\n请提供需要总结的文本，我可以帮你提取要点、生成摘要～"
        if '大纲' in query:
            return "## 大纲制定\n\n告诉我主题，我可以帮你制定结构化框架～"
        return "我可以帮你润色、总结、制定大纲等，请提供具体内容～"

    def _default_response(self, query: str) -> str:
        """默认回复 - 尽量给出有用信息"""
        
        # 问题太短
        if len(query) < 4:
            return f"""## {self.name} 的分析

你提到「{query}」，能再多说点吗？

比如：
- 具体是什么情况？
- 遇到了什么问题？
- 想达到什么目的？

说得越详细，我越能帮到你～"""

        # 一般问题，尝试给出通用建议
        return f"""## {self.name} 的分析

关于「{query}」，我给你一些通用建议：

**分析思路**:
1. 先明确你的目标是什么
2. 列出当前面临的困难
3. 找出可以调动的资源
4. 制定可行的行动计划

**行动建议**:
- 从小事做起，别想一口吃成胖子
- 遇到问题多查资料，善用搜索引擎
- 找有经验的人请教，少走弯路
- 定期复盘，总结得失

具体到你的情况，可以再多说点细节，我帮你出出主意～"""

    def get_daily_tip(self) -> str:
        tips = [
            "今天也要记得适当休息，效率比时长更重要。",
            "完成一个小任务也是进步，为自己点赞！",
            "遇到困难时，不妨换个角度思考问题。",
            "今天的努力，是明天成功的基石。",
            "照顾好自己，才能更好地照顾他人。",
            "专注当下，不要为未发生的事过度担忧。",
            "适当的运动可以提升心情和效率。"
        ]
        day = datetime.now().weekday()
        base_tip = tips[day % len(tips)]
        
        if self.mood_manager:
            if self.mood_manager.is_empathetic_mode():
                return f"💚 {base_tip} 记得，你已经很好了。"
            elif self.mood_manager.is_efficiency_mode():
                return f"🎯 {base_tip} 保持专注，继续前进。"
            elif self.mood_manager.is_casual_mode():
                return f"😊 {base_tip} 享受当下～"
        
        return f"📌 {base_tip}"
    
    def set_mood_manager(self, mood_manager):
        self.mood_manager = mood_manager
    
    def set_preset_manager(self, preset_manager):
        self.preset_manager = preset_manager
