#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI 助手核心模块 - R3 思考版
像人一样思考，有温度的 AI 助手
"""

import random
from typing import Optional, Dict
from datetime import datetime
from .thinking_engine import ThinkingEngine


class Assistant:
    """AI 助手类 (R3 思考版 - zhangy-chat)"""

    def __init__(self, config: Optional[Dict] = None,
                 mood_manager=None, preset_manager=None,
                 memory_manager=None):
        self.config = config or {}
        self.name = "zhangy-chat"

        # R3 管理器
        self.mood_manager = mood_manager
        self.preset_manager = preset_manager
        self.memory_manager = memory_manager

        # R3 思考引擎
        self.thinking_engine = ThinkingEngine()

        # 知识库 - 让 AI 能回答各种问题
        self.knowledge_base = self._init_knowledge_base()

        # 对话风格配置
        self.response_style = {
            "prefix": "",  # 心情前缀
            "suffix": "",  # 心情后缀
            "emoji": True  # 是否使用表情
        }

    def _init_knowledge_base(self) -> Dict:
        """初始化知识库 - 覆盖生活各方面"""
        return {
            # ==================== 饮食类 ====================
            "饮食": {
                "keywords": ["饿", "吃饭", "吃啥", "做饭", "外卖", "食堂", "早餐", "午餐", "晚餐", "夜宵", "减肥餐"],
                "response": self._get_food_response
            },
            # ==================== 编程类 ====================
            "编程": {
                "keywords": ["编程", "代码", "python", "java", "javascript", "写程序", "bug", "报错", "开发", "程序员", "git", "github"],
                "response": self._get_coding_response
            },
            # ==================== 工作类 ====================
            "工作": {
                "keywords": ["工作", "上班", "辞职", "跳槽", "面试", "老板", "同事", "加班", "工资", "涨薪", "离职"],
                "response": self._get_work_response
            },
            # ==================== 学习类 ====================
            "学习": {
                "keywords": ["学习", "考试", "考研", "考证", "复习", "备考", "挂科", "奖学金", "留学"],
                "response": self._get_study_response
            },
            # ==================== 情感类 ====================
            "情感": {
                "keywords": ["喜欢", "暗恋", "表白", "恋爱", "对象", "单身", "分手", "复合", "相亲", "结婚"],
                "response": self._get_love_response
            },
            # ==================== 健康类 ====================
            "健康": {
                "keywords": ["健康", "运动", "减肥", "健身", "生病", "感冒", "头疼", "发烧", "失眠", "脱发", "熬夜"],
                "response": self._get_health_response
            },
            # ==================== 购物类 ====================
            "购物": {
                "keywords": ["购物", "买", "推荐", "淘宝", "京东", "拼多多", "手机", "电脑", "数码"],
                "response": self._get_shopping_response
            },
            # ==================== 旅行类 ====================
            "旅行": {
                "keywords": ["旅行", "旅游", "出去玩", "景点", "酒店", "机票", "高铁", "攻略", "签证"],
                "response": self._get_travel_response
            },
            # ==================== 情绪类 ====================
            "情绪": {
                "keywords": ["累", "辛苦", "困", "疲惫", "压力", "焦虑", "担心", "害怕", "紧张", "崩溃", "烦", "郁闷"],
                "response": self._get_emotion_response
            },
            # ==================== 无聊类 ====================
            "无聊": {
                "keywords": ["无聊", "没事干", "闲", "打发时间", "剧荒", "游戏"],
                "response": self._get_boredom_response
            },
            # ==================== 金钱类 ====================
            "金钱": {
                "keywords": ["钱", "存款", "理财", "基金", "股票", "借钱", "还钱", "信用卡", "贷款"],
                "response": self._get_money_response
            },
            # ==================== 人际类 ====================
            "人际": {
                "keywords": ["朋友", "社交", "孤独", "孤单", "寂寞", "合不来", "矛盾", "吵架"],
                "response": self._get_social_response
            },
        }

    # ==================== 各类回复生成器 ====================

    def _get_food_response(self, query: str) -> str:
        """饮食类回复"""
        responses = [
            """## 吃饭建议

**快速解决**:
- 点外卖：美团/饿了么，30 分钟送到
- 楼下快餐：10-15 元搞定
- 泡面 + 蛋：5 分钟，加根火腿更香

**健康选择**:
- 自己做饭：少油少盐，营养均衡
- 沙拉 + 鸡胸：减脂期首选
- 杂粮饭 + 蔬菜：饱腹感强

想好吃啥了吗？""",
            """## 🍜 干饭人指南

**不知道吃啥？试试**:
1. 打开外卖软件看推荐
2. 想想昨天吃了啥，换换口味
3. 问问朋友吃的啥

**营养搭配**:
- 蛋白质：肉/蛋/奶/豆制品
- 碳水：米饭/面条/杂粮
- 维生素：蔬菜水果

别凑合，好好吃饭～""",
            """## 🥗 饮食小贴士

**早餐**: 鸡蛋 + 牛奶 + 主食（包子/面包）
**午餐**: 肉 + 菜 + 饭，七分饱
**晚餐**: 清淡为主，别太晚

**少吃**: 油炸、高糖、加工食品
**多喝**: 温水，每天 1.5-2L

今天打算吃啥好吃的？""",
        ]
        return random.choice(responses)

    def _get_coding_response(self, query: str) -> str:
        """编程类回复"""
        return """## 编程建议

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

具体遇到啥问题了？说说看～"""

    def _get_work_response(self, query: str) -> str:
        """工作类回复"""
        return """## 工作建议

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

    def _get_study_response(self, query: str) -> str:
        """学习类回复"""
        return """## 📚 学习建议

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

在准备啥考试？我可以帮你规划～"""

    def _get_love_response(self, query: str) -> str:
        """情感类回复"""
        return """## 💕 情感建议

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

感情方面遇到啥问题了？"""

    def _get_health_response(self, query: str) -> str:
        """健康类回复"""
        return """## 🏃 健康建议

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

*严重的话一定要去医院*

最近身体哪里不舒服？"""

    def _get_shopping_response(self, query: str) -> str:
        """购物类回复"""
        return """## 🛒 购物建议

**买前思考**:
1. 真的需要吗？
2. 使用频率会高吗？
3. 有平替吗？

**省钱技巧**:
- 等促销：618、双 11、双 12
- 比价：同款不同平台差价可能很大
- 返利 APP：能省一点是一点
- 二手平台：闲鱼淘好物

**数码产品**:
- 手机：苹果/华为/小米看预算
- 电脑：办公选轻薄本，游戏选游戏本
- 别买太便宜的，容易踩坑

想买啥？我帮你参谋参谋～"""

    def _get_travel_response(self, query: str) -> str:
        """旅行类回复"""
        return """## ✈️ 旅行建议

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

想去哪玩？我可以帮你做攻略～"""

    def _get_emotion_response(self, query: str) -> str:
        """情绪类回复"""
        # 根据心情调整语气
        if self.mood_manager and self.mood_manager.is_empathetic_mode():
            return """## 💚 情绪疏导

我懂你现在的感受，真的。

这种时候别一个人扛着，说出来会好受点。

**可以试试这样做**:
1. 先深呼吸几次，让自己缓一缓
2. 找信任的人聊聊，别憋着
3. 出去走走，换个环境

**即时缓解**:
- 深呼吸：吸气 4 秒，憋气 7 秒，呼气 8 秒
- 听点轻音乐，放松一下
- 洗个热水澡，好好睡一觉

记住：你不是一个人，有需要随时找我～"""

        return """## 💚 情绪疏导

**即时缓解**:
- 深呼吸：吸气 4 秒，憋气 7 秒，呼气 8 秒
- 出去走走，换个环境
- 找人聊聊，别憋着

**长期调节**:
- 运动：跑步、游泳、瑜伽
- 冥想：每天 10 分钟
- 保证睡眠

**调整心态**:
- 很多事没你想的那么严重
- 别追求完美，够好就行
- 你已经在努力了，这很重要

压力大的时候记得找我聊聊～"""

    def _get_boredom_response(self, query: str) -> str:
        """无聊类回复"""
        return """## 🎮 无聊时可以做的事

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

    def _get_money_response(self, query: str) -> str:
        """金钱类回复"""
        return """## 💰 金钱建议

**存钱**:
- 每月强制存 20%-30%
- 先存后花，别先花后存
- 记账，知道钱花哪了

**理财**:
- 余额宝/零钱通：放日常开销
- 定期存款：保本保息
- 基金：定投指数基金，长期持有
- 股票：风险高，别 All in

**消费**:
- 大额消费等 3 天再决定
- 办卡要谨慎
- 别碰网贷

有具体理财问题可以问我～"""

    def _get_social_response(self, query: str) -> str:
        """人际类回复"""
        return """## 🤝 社交建议

**交朋友**:
- 参加兴趣活动，认识志同道合的人
- 主动一点，先从打招呼开始
- 真诚待人，别太功利

**处理矛盾**:
- 冷静下来再沟通
- 换位思考，理解对方
- 该道歉就道歉，别硬撑

**独处**:
- 一个人不等于孤独
- 培养爱好，充实自己
- 享受独处的时光

**社交焦虑**:
- 从小圈子开始
- 不用讨好所有人
- 做真实的自己

遇到啥社交问题了？说说看～"""

    # ==================== 主对话方法 ====================

    def chat(self, query: str, context: Optional[Dict] = None) -> str:
        """
        通用对话 - 像人一样思考（R3 思考版）

        Args:
            query: 用户问题
            context: 上下文信息（可选）

        Returns:
            zhangy-chat 的回复
        """
        # R3 思考引擎：先思考再回应
        thinking_result = self.thinking_engine.think(query, context)

        # 1. 检查简单对话（无需思考）
        simple_response = self._check_simple_query(query)
        if simple_response:
            return self._format_response(simple_response, thinking_result)

        # 2. 检查知识库匹配 + 思考式优化
        for category, data in self.knowledge_base.items():
            for keyword in data["keywords"]:
                if keyword in query:
                    base_response = data["response"](query)
                    # 思考式优化：添加个性化建议
                    optimized_response = self._optimize_with_thinking(base_response, thinking_result)
                    return self._format_response(optimized_response, thinking_result)

        # 3. 通用回复 - 思考式回应
        return self._thoughtful_response(query, thinking_result)

    def _format_response(self, response: str, thinking_result: Dict) -> str:
        """格式化回复（添加思考式前缀）"""
        # 如果思考模式开启且需要显示思考过程
        if self.thinking_engine.thinking_mode and self.thinking_engine.show_thinking_process:
            summary = self.thinking_engine.get_thinking_summary(thinking_result)
            if summary:
                return f"zhangy-chat：[思考]{summary}\n\n{response}"
        return f"zhangy-chat：{response}"

    def _optimize_with_thinking(self, base_response: str, thinking_result: Dict) -> str:
        """基于思考结果优化回复"""
        personalization = thinking_result.get("personalization", {})
        
        # 如果需要先共情
        if personalization.get("structure") == "empathy_first":
            emotion = thinking_result.get("emotion", {})
            if emotion.get("needs_empathy"):
                empathy_prefix = self._get_empathy_prefix(emotion.get("emotion", "neutral"))
                return f"{empathy_prefix}\n\n---\n\n{base_response}"
        
        return base_response

    def _get_empathy_prefix(self, emotion: str) -> str:
        """获取共情前缀"""
        empathy_map = {
            "anxious": "我理解你现在的感受，这种担心是很正常的。先深呼吸一下，我们慢慢来分析。",
            "frustrated": "换谁遇到这种事都会觉得烦，你的感受我懂。别憋着，说出来会好受点。",
            "tired": "辛苦了，忙到现在确实该歇歇了。身体最重要，不用有负罪感。",
            "angry": "这事换谁都会生气的，你生气是完全合理的。先消消气，咱们一起想想怎么办。",
        }
        return empathy_map.get(emotion, "我理解你的感受，咱们一起来看看怎么解决。")

    def _check_simple_query(self, query: str) -> Optional[str]:
        """检查简单对话"""
        simple_responses = {
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
            "开心": "开心就好！保持好心情～",
            "难过": "怎么了？想聊聊吗？我在这里陪着你。",
            "我想死": """我真的很担心你。

我知道你现在一定很难受，但请相信，再难的事情都会过去的。

**可以试试这样做**:
1. 先深呼吸几次，让自己缓一缓
2. 找信任的人聊聊，别一个人扛着
3. 拨打心理援助热线：400-161-9995（24 小时）

你不是一个人，还有人在乎你。如果需要聊聊，我随时都在。""",
            "不想活了": """我很担心你的状态。

这种感受一定很不好受，但请给自己一个机会。

**现在可以做**:
1. 联系信任的家人或朋友
2. 拨打心理援助热线：400-161-9995
3. 去最近的医院心理科

你很重要，这个世界需要你。""",
        }

        for key, response in simple_responses.items():
            if key in query:
                return response
        return None

    def _thoughtful_response(self, query: str, thinking_result: Dict) -> str:
        """通用回复 - 思考式回应"""
        # 基于思考结果生成有针对性的回复
        needs = thinking_result.get("needs", {})
        emotion = thinking_result.get("emotion", {})
        
        # 如果有情绪需求，先共情
        if emotion.get("needs_empathy"):
            empathy = self._get_empathy_prefix(emotion.get("emotion", "neutral"))
            analysis = self._get_analysis_content(query, needs)
            return f"zhangy-chat：{empathy}\n\n---\n\n{analysis}"
        
        # 直接分析
        analysis = self._get_analysis_content(query, needs)
        return f"zhangy-chat：{analysis}"

    def _get_analysis_content(self, query: str, needs: Dict) -> str:
        """获取分析内容"""
        core_ask = needs.get("core_ask", query[:50])
        
        return f"""## {self.name} 的分析

关于「{core_ask}」，我来帮你分析一下：

**分析思路**:
1. 先明确核心问题是什么
2. 找出关键影响因素
3. 梳理各因素之间的关系

**建议**:
- 复杂问题拆成小问题逐个突破
- 多问几个"为什么"找到根本原因
- 必要时寻求专业意见

你能再多说点具体情境吗？这样我能给到更有针对性的建议～"""

    def _apply_mood_style(self, response: str) -> str:
        """根据心情调整回复风格"""
        if not self.mood_manager:
            return response

        prefix = self.mood_manager.get_response_prefix()
        suffix = self.mood_manager.get_response_suffix()

        parts = []
        if prefix:
            parts.append(prefix)
        parts.append(response)
        if suffix:
            parts.append(suffix)

        return "\n\n".join(parts)

    def get_daily_tip(self) -> str:
        """每日小贴士"""
        tips = [
            "今天也要记得适当休息，效率比时长更重要。",
            "完成一个小任务也是进步，为自己点赞！",
            "遇到困难时，不妨换个角度思考问题。",
            "今天的努力，是明天成功的基石。",
            "照顾好自己，才能更好地照顾他人。",
            "专注当下，不要为未发生的事过度担忧。",
            "适当的运动可以提升心情和效率。",
        ]
        day = datetime.now().weekday()
        base_tip = tips[day % len(tips)]

        if self.mood_manager:
            if self.mood_manager.is_empathetic_mode():
                return f"💡 {base_tip} 记得，你已经很好了。"
            elif self.mood_manager.is_efficiency_mode():
                return f"🎯 {base_tip} 保持专注，继续前进。"

        return f"💡 {base_tip}"

    def set_mood_manager(self, mood_manager):
        self.mood_manager = mood_manager

    def set_preset_manager(self, preset_manager):
        self.preset_manager = preset_manager
