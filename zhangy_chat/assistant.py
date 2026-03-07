#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI 助手核心模块 - R4 实用版
啥问题都能答，不再套模板
"""

from typing import Optional, Dict
from .logic_engine import LogicEngine
from .emotion_engine import EmotionEngine


class Assistant:
    """AI 助手类 (R4 实用版)"""

    def __init__(self, config: Optional[Dict] = None, 
                 mood_manager=None, preset_manager=None,
                 memory_manager=None):
        self.config = config or {}
        self.name = self.config.get('personality', {}).get('name', 'zhangy')
        
        # 管理器
        self.mood_manager = mood_manager
        self.preset_manager = preset_manager
        self.memory_manager = memory_manager
        
        # 引擎
        self.logic_engine = LogicEngine()
        self.emotion_engine = EmotionEngine()
        
        # 超大全实用回复库 - 覆盖生活各方面
        self.practical_responses = {
            # 饮食类
            "饿": {
                "keywords": ["饿", "吃饭", "吃东西", "肚子", "食堂", "外卖", "做饭", "早餐", "午餐", "晚餐"],
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
2. 想想昨天吃了啥，换换口味
3. 问问朋友吃的啥

想好吃啥了吗？"""
            },
            # 编程类
            "编程": {
                "keywords": ["编程", "代码", "python", "java", "写程序", "开发", "bug", "报错"],
                "response": """## 💻 编程建议

**学习路线**:
- 入门：Python（语法简单，应用广）
- 前端：HTML/CSS → JavaScript → Vue/React
- 后端：Java/Go/Node.js + 数据库
- 数据：Python + SQL + 机器学习

**常见问题**:
- 环境配置：用 Anaconda 管理 Python 环境
- 代码报错：先看错误信息最后一行
- 记不住语法：多敲代码，自然就会了

**接私活**:
- 猪八戒网、程序员客栈
- 先从小项目开始，积累口碑
- 报价别太低，不然累死还不赚钱

具体遇到啥问题了？说说看～"""
            },
            # 工作类
            "工作": {
                "keywords": ["工作", "上班", "职场", "老板", "同事", "加班", "辞职", "跳槽", "面试", "工资"],
                "response": """## 💼 工作建议

**职场生存**:
- 少说话多做事，尤其是新人
- 和同事保持距离，别太亲近也别太疏远
- 老板画饼听听就好，实际利益最重要

**涨薪技巧**:
- 跳槽涨薪最快（30%-50%）
- 内部调薪慢（10%-20%）
- 有 offer 再谈涨薪，底气足

**关于跳槽**:
- 干得不开心就先骑驴找马
- 拿到 offer 再提离职
- 金三银四、金九银十是跳槽季

**加班**:
- 偶尔加班正常，长期 996 要跑
- 加班没加班费就是白嫖
- 身体最重要，别硬撑

工作上遇到啥事了？可以跟我吐槽～"""
            },
            # 学习类
            "学习": {
                "keywords": ["学习", "考试", "复习", "备考", "考研", "考证", "挂科", "奖学金"],
                "response": """## 📚 学习建议

**高效方法**:
- 番茄钟：25 分钟专注 +5 分钟休息
- 费曼技巧：尝试给别人讲懂
- 错题本：记录易错点，定期复习

**备考建议**:
1. 先做一套真题，了解难度和题型
2. 制定复习计划，倒推时间节点
3. 重点突破，不要平均用力
4. 考前模拟，适应考试节奏

**考研**:
- 确定目标院校和专业
- 英语和政治要过线
- 专业课是拉分关键
- 报不报班看自律能力

**考证**:
- 英语四六级必考
- 计算机二级有用
- 专业证书看行业需求

在准备啥考试？我可以帮你规划～"""
            },
            # 情感类
            "情感": {
                "keywords": ["喜欢", "暗恋", "表白", "恋爱", "对象", "单身", "分手", "复合", "相亲"],
                "response": """## 💕 情感建议

**暗恋阶段**:
- 先当朋友处，多接触多了解
- 观察对方对你有没有特殊对待
- 时机成熟再表白，别太急

**表白**:
- 私下表白，别当众
- 真诚最重要，别搞花里胡哨
- 做好被拒绝的心理准备

**恋爱中**:
- 多沟通，别让猜来猜去
- 给彼此空间，别太黏
- 小矛盾别上纲上线

**分手**:
- 难过是正常的，别憋着
- 时间会治愈一切
- 下一个会更好

**单身**:
- 先过好自己，花若盛开蝴蝶自来
- 多参加社交活动，扩大圈子
- 别将就，宁缺毋滥

感情方面遇到啥问题了？"""
            },
            # 健康类
            "健康": {
                "keywords": ["健康", "运动", "减肥", "健身", "生病", "感冒", "头疼", "发烧", "失眠", "脱发"],
                "response": """## 💚 健康建议

**减肥**:
- 管住嘴比迈开腿重要
- 戒掉零食和夜宵
- 高蛋白 + 适量碳水 + 大量蔬菜
- 每周减 0.5-1kg 是健康速度

**运动**:
- 每周 150 分钟中等强度运动
- 力量训练 2-3 次/周
- 跑步、游泳、跳绳都可以

**睡眠**:
- 保证 7-8 小时睡眠
- 11 点前睡觉，别熬夜
- 睡前 1 小时不用电子设备

**小毛病**:
- 感冒：多喝水，维 C 泡腾片
- 头疼：休息，别硬撑
- 失眠：泡脚、喝牛奶、听轻音乐
- 脱发：少熬夜，用生姜洗发水

*严重的话一定要去医院*

最近身体哪里不舒服？"""
            },
            # 购物类
            "购物": {
                "keywords": ["购物", "买", "推荐", "好物", "淘宝", "京东", "拼多多", "手机", "电脑"],
                "response": """## 🛒 购物建议

**买前思考**:
1. 真的需要吗？
2. 使用频率会高吗？
3. 有平替吗？

**省钱技巧**:
- 等促销：618、双 11、双 12
- 比价：同款不同平台差价可能很大
- 返利 APP：能省一点是一点
- 二手平台：闲鱼淘好物

**避坑**:
- 看差评，别看好评
- 注意退换货政策
- 警惕"限时抢购"套路

**数码产品**:
- 手机：苹果/华为/小米看预算
- 电脑：办公选轻薄本，游戏选游戏本
- 别买太便宜的，容易踩坑

想买啥？我帮你参谋参谋～"""
            },
            # 旅行类
            "旅行": {
                "keywords": ["旅行", "旅游", "出去玩", "景点", "酒店", "机票", "高铁", "攻略"],
                "response": """## ✈️ 旅行建议

**目的地选择**:
- 预算少：周边城市/省内
- 时间紧：选一个城市深度游
- 想放松：海边/山区度假村

**省钱技巧**:
- 机票：提前 1-2 个月买，周二下午最便宜
- 酒店：多平台对比，看差评
- 门票：学生证/老年证有优惠
- 高铁票：提前 15 天抢票

**必备物品**:
- 证件：身份证/学生证
- 电子：充电宝、充电器
- 药品：感冒药、肠胃药、创可贴
- 衣物：查好天气再带

**攻略制作**:
1. 确定想去的地方
2. 按区域分组，减少路途
3. 别排太满，留休息时间

想去哪玩？我可以帮你做攻略～"""
            },
            # 无聊类
            "无聊": {
                "keywords": ["无聊", "没事干", "闲", "打发时间", "剧荒", "游戏"],
                "response": """## 🎮 无聊时可以做的事

**宅家**:
- 刷剧：豆瓣高分榜照着看
- 看书：微信读书免费看
- 打游戏：放松一下
- 学做菜：从简单的开始
- 大扫除：整理房间很解压

**出门**:
- 公园散步
- 博物馆/美术馆
- 电影院
- 健身房
- 约朋友吃饭聊天

**提升自己**:
- 学个技能（PS/剪辑/外语）
- 健身减肥
- 考个证
- 看纪录片涨知识

想干啥类型的？我帮你具体推荐～"""
            },
            # 累类
            "累": {
                "keywords": ["累", "辛苦", "困", "乏", "疲惫", "熬夜", "透支"],
                "response": """## 😴 累了就休息休息

**快速恢复**:
- 小睡 20 分钟
- 洗个热水澡
- 听点轻音乐
- 出去走走，呼吸新鲜空气

**长期调节**:
- 保证睡眠，别熬夜
- 适当运动，出出汗
- 周末彻底放松一天
- 定期休假，别连轴转

**心理调节**:
- 别给自己太大压力
- 该躺平的时候就躺平
- 工作不是生活的全部
- 学会拒绝，别什么都接

**熬夜**:
- 偶尔熬夜没事，别长期
- 熬夜后补觉 + 多喝水
- 第二天别开车，容易出事

最近是不是太辛苦了？好好休息休息吧～"""
            },
            # 压力类
            "压力": {
                "keywords": ["压力", "焦虑", "紧张", "担心", "害怕", "崩溃"],
                "response": """## 💚 压力大的时候

**即时缓解**:
- 深呼吸：吸气 4 秒，憋气 7 秒，呼气 8 秒
- 出去走走，换个环境
- 找人聊聊，别憋着
- 哭出来不丢人

**长期调节**:
- 运动：跑步、游泳、瑜伽
- 冥想：每天 10 分钟
- 保证睡眠
- 培养爱好

**调整心态**:
- 很多事没你想的那么严重
- 别追求完美，够好就行
- 你已经在努力了，这很重要

**寻求帮助**:
- 找朋友家人聊聊
- 必要时看心理咨询师
- 心理热线：12355（青少年）

记住：你不是一个人，有需要随时找我～"""
            },
            # 金钱类
            "金钱": {
                "keywords": ["钱", "工资", "存款", "理财", "基金", "股票", "借钱", "还钱"],
                "response": """## 💰 金钱建议

**存钱**:
- 每月强制存 20%-30%
- 先存后花，别先花后存
- 记账，知道钱花哪了

**理财**:
- 余额宝/零钱通：放日常开销
- 定期存款：保本保息
- 基金：定投指数基金，长期持有
- 股票：风险高，别 All in

**借钱**:
- 借急不借穷
- 写好借条
- 做好要不回来的准备

**消费**:
- 大额消费等 3 天再决定
- 办卡要谨慎
- 别碰网贷

有具体理财问题可以问我～"""
            }
        }
        
        # 简单对话库
        self.simple_queries = {
            "你叫什么": f"我叫 {self.name}，是你的专属 AI 助手～",
            "你是谁": f"我是 {self.name}，一个本地 AI 助手，可以帮你管理任务、规划目标、聊天解闷～",
            "你能做什么": "我能帮你：1) 管理任务和 goal 2) 解答各种问题 3) 聊天解闷 4) 给建议。有啥需要尽管说～",
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
            "无聊": "无聊的话，可以看看书、运动一下，或者跟我聊聊天呀～",
            "开心": "开心就好！保持好心情～",
            "难过": "怎么了？想聊聊吗？我在这里陪着你。"
        }

    def chat(self, query: str) -> str:
        """通用对话 - 优先级：简单对话 > 情感 > 实用 > 逻辑推理 > 默认"""
        
        # 1. 简单对话
        for key, response in self.simple_queries.items():
            if key in query:
                return self._apply_emotion_style(response)
        
        # 2. 情感识别
        emotion_result = self.emotion_engine.recognize(query)
        
        # 3. 实用回复（超全库）
        practical_response = self._check_practical_query(query)
        if practical_response:
            return self._apply_emotion_style(practical_response)
        
        # 4. 逻辑推理
        logic_result = self.logic_engine.analyze(query, {
            "emotion": emotion_result["emotion"],
            "intensity": emotion_result["intensity"]
        })
        
        # 5. 整合回复
        return self._integrate_response(logic_result, emotion_result, query)
    
    def _check_practical_query(self, query: str) -> Optional[str]:
        """检查实用回复库"""
        for category, data in self.practical_responses.items():
            for keyword in data["keywords"]:
                if keyword in query:
                    return data["response"]
        return None
    
    def _integrate_response(self, logic_result: Dict, emotion_result: Dict, 
                           original_query: str) -> str:
        """整合逻辑推理和情感回应"""
        emotion = emotion_result["emotion"]
        logic_content = logic_result.get("content", "")
        
        # 判断是否需要情感回应
        if not self.emotion_engine.should_adjust_response(logic_content):
            return logic_content
        
        # 获取情感回应
        emotion_response = self.emotion_engine.respond(
            emotion, original_query, logic_content
        )
        
        # 负面情绪：先共情，再解答
        if emotion in ["anxiety", "frustrated", "angry", "tired", "overwhelmed", "lonely"]:
            return f"""{emotion_response}

---

**关于你说的这件事**，我来帮你分析一下：

{logic_content}"""
        
        # 正面情绪：先共鸣
        elif emotion in ["happy", "proud"]:
            return f"""{emotion_response}

{logic_content}"""
        
        else:
            return logic_content
    
    def _apply_emotion_style(self, response: str) -> str:
        """根据心情管理器调整风格"""
        if self.mood_manager:
            prefix = self.mood_manager.get_response_prefix()
            suffix = self.mood_manager.get_response_suffix()
            
            if self.mood_manager.is_efficiency_mode():
                response = response.split('\n\n---\n')[0]
            
            parts = []
            if prefix:
                parts.append(prefix)
            parts.append(response)
            if suffix:
                parts.append(suffix)
            
            return "\n\n".join(parts)
        
        return response
    
    # 逻辑推理专用
    def logic_chat(self, query: str) -> str:
        """纯逻辑推理模式"""
        result = self.logic_engine.analyze(query)
        return result.get("content", "这个问题我需要更多信息才能分析。")
    
    # 情感管理
    def get_emotion_status(self) -> str:
        return self.emotion_engine.get_emotion_summary()
    
    def clear_emotion_memory(self) -> str:
        return self.emotion_engine.clear_memory()
    
    def set_emotion_intensity(self, level: str) -> bool:
        return self.emotion_engine.set_intensity_level(level)
    
    def get_daily_tip(self) -> str:
        from datetime import datetime
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
        
        return f"📌 {base_tip}"
    
    def set_mood_manager(self, mood_manager):
        self.mood_manager = mood_manager
    
    def set_preset_manager(self, preset_manager):
        self.preset_manager = preset_manager
