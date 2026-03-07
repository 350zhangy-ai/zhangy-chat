#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CMD 命令行界面模块（R4 深度智能版）
新增：逻辑推理指令、情感管理指令
"""

import sys
import argparse
from typing import Optional
from .task_manager import TaskManager
from .data_manager import DataManager
from .assistant import Assistant
from .memory_manager import MemoryManager
from .mood_manager import MoodManager
from .preset_manager import PresetManager


class CMDInterface:
    """CMD 命令行界面 (R4)"""

    def __init__(self):
        self.task_manager = TaskManager()
        self.data_manager = DataManager()

        # R3 管理器
        self.memory_manager = MemoryManager()
        self.mood_manager = MoodManager()
        self.preset_manager = PresetManager()

        # 初始化助手并注入管理器
        self.assistant = Assistant(
            mood_manager=self.mood_manager,
            preset_manager=self.preset_manager
        )

        self.running = True

    def run(self):
        """运行 CMD 界面"""
        print("=" * 50)
        print("  Zhangy Chat R4 - 深度智能版")
        print("  输入 /help 查看指令，/gui 切换图形界面，exit 退出")
        print("=" * 50)

        # 显示当前配置
        self._show_status()

        while self.running:
            try:
                cmd = input("\n> ").strip()
                if not cmd:
                    continue

                if cmd.startswith('/'):
                    self._handle_command(cmd)
                else:
                    # 普通对话，交给 AI 助手（含情感识别和逻辑推理）
                    response = self.assistant.chat(cmd)
                    print(response)

            except KeyboardInterrupt:
                print("\n再见！")
                break
            except Exception as e:
                print(f"错误：{e}")
    
    def _show_status(self):
        """显示当前状态"""
        mem_info = self.memory_manager.get_memory_info()
        mood_info = self.mood_manager.get_mood_info()
        preset_info = self.preset_manager.BUILTIN_PRESETS.get(
            self.preset_manager.get_current_preset(), {}
        )
        
        print(f"\n当前配置:")
        print(f"  内存：{mem_info['selected']}GiB (实际：{mem_info['actual']}GiB)")
        print(f"  心情：{mood_info['icon']} {mood_info['name']}")
        print(f"  预设：{preset_info.get('icon', '📁')} {preset_info.get('name', '未知')}")
        print(f"  情感强度：{self.assistant.emotion_engine.emotion_intensity_level}")

    def _handle_command(self, cmd: str):
        """处理指令"""
        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        commands = {
            '/help': self._cmd_help,
            '/add': self._cmd_add_task,
            '/del': self._cmd_del_task,
            '/list': self._cmd_list_tasks,
            '/mark': self._cmd_mark_task,
            '/goal': self._cmd_goal,
            '/review': self._cmd_review,
            '/progress': self._cmd_progress,
            '/habit': self._cmd_habit,
            '/backup': self._cmd_backup,
            '/restore': self._cmd_restore,
            '/export': self._cmd_export,
            '/gui': self._cmd_gui,
            '/exit': self._cmd_exit,
            '/quit': self._cmd_exit,
            # R3 指令
            '/mem': self._cmd_mem,
            '/mood': self._cmd_mood,
            '/preset': self._cmd_preset,
            '/status': self._cmd_status,
            # R4 新增指令
            '/logic': self._cmd_logic,
            '/emotion': self._cmd_emotion,
            # R5 新增指令
            '/reason': self._cmd_reason
        }

        handler = commands.get(command)
        if handler:
            handler(args)
        else:
            print(f"未知指令：{command}")
            print("输入 /help 查看可用指令")

    def _cmd_help(self, args: str):
        """帮助指令"""
        help_text = """
可用指令:
  任务管理:
    /add <标题> [描述]           添加任务
    /del <ID>                   删除任务
    /list [状态]                查看任务
    /mark <ID> <状态>           标记任务状态

  目标规划:
    /goal add <标题> [描述]      添加目标
    /goal list                  查看目标
    /goal milestone <ID> <内容>  添加里程碑
    /review [天数]              生成复盘报告
    /progress <ID>              查看目标进度

  习惯打卡:
    /habit add <名称> [频率]     添加习惯
    /habit list                 查看习惯
    /habit check <ID>           打卡

  数据管理:
    /backup [名称]              备份数据
    /restore <名称>             恢复备份
    /export <格式>              导出数据 (txt/excel/csv)

  R3 配置:
    /mem [8/16/32/64]           设置内存配置
    /mood [心情]                设置心情
    /preset [预设]              切换预设
    /status                     查看当前状态

  R4 新增:
    /logic <问题>               逻辑推理模式解答问题
    /emotion check              查看情感状态
    /emotion clear              清除情感记忆
    /emotion level [弱/中/强]   设置情感强度

  R5 新增:
    /reason <问题>              深度推理模式（分步推理 + 自我检查）

  其他:
    /gui                        切换至图形界面
    /exit                       退出程序
"""
        print(help_text)

    # R4 新增指令
    def _cmd_logic(self, args: str):
        """逻辑推理指令"""
        if not args:
            print("用法：/logic <问题>")
            print("示例：/logic 为什么加班越久效率越低")
            print("      /logic 为什么坚持很难")
            return
        
        response = self.assistant.logic_chat(args)
        print(response)

    def _cmd_reason(self, args: str):
        """深度推理指令（参考 DeepSeek-R1）"""
        if not args:
            print("用法：/reason <问题>")
            print("示例：/reason 要不要辞职")
            print("      /reason 如何选择合适的城市")
            print("\n深度推理模式会：")
            print("1. 分步推理问题")
            print("2. 自我检查推理过程")
            print("3. 给出结论和建议")
            return
        
        response = self.assistant.deep_reasoning(args)
        print(response)

    def _cmd_emotion(self, args: str):
        """情感管理指令"""
        if not args:
            print("用法：/emotion <子指令>")
            print("子指令:")
            print("  check  - 查看情感状态")
            print("  clear  - 清除情感记忆")
            print("  level [弱/中/强] - 设置情感强度")
            return
        
        parts = args.split(maxsplit=1)
        subcmd = parts[0].lower()
        subargs = parts[1] if len(parts) > 1 else ""
        
        if subcmd == "check":
            summary = self.assistant.get_emotion_status()
            print(summary)
        
        elif subcmd == "clear":
            msg = self.assistant.clear_emotion_memory()
            print(msg)
        
        elif subcmd == "level":
            level_map = {"弱": "weak", "中": "medium", "强": "strong"}
            level = level_map.get(subargs, subargs.lower())
            if self.assistant.set_emotion_intensity(level):
                print(f"✓ 情感强度已设置为 {subargs or level}")
            else:
                print("用法：/emotion level [弱/中/强]")
        
        else:
            print(f"未知子指令：{subcmd}")

    # R3 指令保持不变
    def _cmd_mem(self, args: str):
        """内存配置指令"""
        if not args:
            mem_info = self.memory_manager.get_memory_info()
            print(f"当前内存配置:")
            print(f"  已选择：{mem_info['selected']}GiB")
            print(f"  实际物理内存：{mem_info['actual']}GiB")
            print(f"  缓存大小：{mem_info['config']['cache_size']}MB")
            print(f"  最大并发：{mem_info['config']['max_concurrent']}")
            print(f"  数据加载：{mem_info['config']['data_loading']}")
            return
        
        try:
            mem_gib = int(args.strip())
            result = self.memory_manager.set_memory(mem_gib)
            
            if result['success']:
                print(f"✓ {result['message']}")
                print(f"  缓存：{result['config']['cache_size']}MB")
                print(f"  并发：{result['config']['max_concurrent']}")
            else:
                print(f"⚠ {result['message']}")
                if 'current' in result:
                    print(f"  当前已降级为：{result['current']}GiB")
        except ValueError:
            print("用法：/mem [8/16/32/64]")

    def _cmd_mood(self, args: str):
        """心情设置指令"""
        if not args:
            mood_info = self.mood_manager.get_mood_info()
            print(f"当前心情：{mood_info['icon']} {mood_info['name']}")
            print(f"风格：{mood_info['style']}")
            print("\n可用心情:")
            for key, info in self.mood_manager.get_all_moods().items():
                marker = "✓" if key == self.mood_manager.get_current_mood() else " "
                print(f"  {marker} {info['icon']} {info['name']} (/{key})")
            return
        
        mood_map = {
            '焦虑': 'anxious', '低落': 'anxious',
            '高效': 'focused', '专注': 'focused',
            '轻松': 'relaxed', '愉悦': 'relaxed',
            '平静': 'calm', '温和': 'calm',
            '疲惫': 'tired', '休息': 'tired'
        }
        
        mood_key = args.strip().lower()
        if mood_key in mood_map:
            mood_key = mood_map[mood_key]
        
        result = self.mood_manager.set_mood(mood_key)
        
        if result['success']:
            print(f"✓ {result['message']}")
            print(f"  回应风格：{result['style']}")
        else:
            print(f"⚠ {result['message']}")

    def _cmd_preset(self, args: str):
        """预设管理指令"""
        if not args:
            presets = self.preset_manager.get_all_presets()
            print("可用预设:")
            for p in presets:
                marker = "✓" if p['is_active'] else " "
                custom_tag = " [自定义]" if p['is_custom'] else ""
                print(f"  {marker} {p['icon']} {p['name']}{custom_tag}")
                print(f"      {p['description']}")
            return
        
        parts = args.split(maxsplit=2)
        subcmd = parts[0].lower()
        
        preset_map = {
            '办公': 'office', '工作': 'office',
            '备考': 'exam', '学习': 'exam',
            '陪伴': 'casual', '休闲': 'casual',
            '疏导': 'emotional', '情绪': 'emotional'
        }
        
        if subcmd == "add":
            if len(parts) < 2:
                print("用法：/preset add <预设名称>")
                return
            name = parts[1]
            result = self.preset_manager.add_custom_preset(
                name=name,
                config={"focus_mode": True}
            )
            if result['success']:
                print(f"✓ {result['message']}")
                print(f"  预设键：{result['preset_key']}")
            else:
                print(f"⚠ {result['message']}")
        
        elif subcmd == "del":
            if len(parts) < 2:
                print("用法：/preset del <预设名称>")
                return
            preset_key = parts[1]
            result = self.preset_manager.delete_custom_preset(preset_key)
            if result['success']:
                print(f"✓ {result['message']}")
            else:
                print(f"⚠ {result['message']}")
        
        else:
            preset_key = subcmd
            if preset_key in preset_map:
                preset_key = preset_map[preset_key]
            
            result = self.preset_manager.set_preset(preset_key)
            if result['success']:
                print(f"✓ {result['message']}")
            else:
                print(f"⚠ {result['message']}")

    def _cmd_status(self, args: str):
        """查看状态指令"""
        self._show_status()

    # 原有任务、目标、习惯、数据管理指令保持不变
    def _cmd_add_task(self, args: str):
        """添加任务"""
        if not args:
            print("用法：/add <任务标题> [任务描述]")
            return
        parts = args.split(maxsplit=1)
        title = parts[0]
        description = parts[1] if len(parts) > 1 else ""
        task = self.task_manager.add_task(title, description)
        print(f"✓ 任务已添加 [ID: {task.id}]")

    def _cmd_del_task(self, args: str):
        """删除任务"""
        if not args:
            print("用法：/del <任务 ID>")
            return
        if self.task_manager.delete_task(args.strip()):
            print(f"✓ 任务 {args.strip()} 已删除")
        else:
            print(f"未找到任务：{args.strip()}")

    def _cmd_list_tasks(self, args: str):
        """列出任务"""
        status = args.strip() if args.strip() else "pending"
        if status == "all":
            tasks = self.task_manager.get_tasks()
        else:
            tasks = self.task_manager.get_tasks(status=status)
        if not tasks:
            print("暂无任务")
            return
        print(f"{'ID':<10} {'标题':<20} {'状态':<10} {'优先级':<6}")
        print("-" * 50)
        for task in tasks:
            status_map = {"pending": "待完成", "completed": "已完成", 
                         "in_progress": "进行中", "cancelled": "已取消"}
            print(f"{task.id:<10} {task.title[:20]:<20} {status_map.get(task.status, '未知'):<10} {task.priority:<6}")

    def _cmd_mark_task(self, args: str):
        """标记任务状态"""
        parts = args.split()
        if len(parts) < 2:
            print("用法：/mark <任务 ID> <状态>")
            return
        task_id, status = parts[0], parts[1]
        if self.task_manager.update_task_status(task_id, status):
            print(f"✓ 任务 {task_id} 状态已更新为 {status}")
        else:
            print(f"未找到任务：{task_id}")

    def _cmd_goal(self, args: str):
        """目标管理"""
        if not args:
            print("用法：/goal add <标题> [描述]")
            print("      /goal list")
            print("      /goal milestone <ID> <内容>")
            return
        parts = args.split(maxsplit=2)
        subcmd = parts[0].lower()
        if subcmd == "add":
            if len(parts) < 2:
                print("用法：/goal add <目标标题> [描述]")
                return
            title = parts[1]
            desc = parts[2] if len(parts) > 2 else ""
            goal = self.task_manager.add_goal(title, desc)
            print(f"✓ 目标已添加 [ID: {goal.id}]")
        elif subcmd == "list":
            goals = self.task_manager.get_goals()
            if not goals:
                print("暂无目标")
                return
            print(f"{'ID':<10} {'标题':<20} {'状态':<10} {'进度':<10}")
            print("-" * 55)
            for goal in goals:
                progress = goal.get_progress()
                print(f"{goal.id:<10} {goal.title[:20]:<20} {goal.status:<10} {progress:.0f}%")
        elif subcmd == "milestone":
            if len(parts) < 3:
                print("用法：/goal milestone <目标 ID> <里程碑内容>")
                return
            goal_id, milestone = parts[1], parts[2]
            if self.task_manager.add_milestone(goal_id, milestone):
                print(f"✓ 里程碑已添加")
            else:
                print(f"未找到目标：{goal_id}")

    def _cmd_review(self, args: str):
        """生成复盘报告"""
        days = int(args.strip()) if args.strip() else 7
        review = self.task_manager.generate_review(days)
        print(f"\n{'='*40}")
        print(f"  复盘报告：{review['period']}")
        print(f"{'='*40}\n")
        print(f"✅ 完成任务：{review['completed_tasks']} 个")
        for task in review['task_details'][:5]:
            print(f"   - {task['title']}")
        print(f"\n🎯 进行中目标：{review['active_goals']} 个")
        for goal in review['goal_progress']:
            print(f"   - {goal['title']}: {goal['progress']:.0f}%")
        print(f"\n📊 习惯打卡:")
        for habit in review['habits_summary']:
            print(f"   - {habit['title']}: 连续{habit['streak']}天，总计{habit['total']}次")

    def _cmd_progress(self, args: str):
        """查看目标进度"""
        if not args:
            print("用法：/progress <目标 ID>")
            return
        progress = self.task_manager.get_goal_progress(args.strip())
        if progress is not None:
            print(f"目标进度：{progress:.1f}%")
        else:
            print(f"未找到目标：{args.strip()}")

    def _cmd_habit(self, args: str):
        """习惯管理"""
        if not args:
            print("用法：/habit add <名称> [频率]")
            print("      /habit list")
            print("      /habit check <ID>")
            return
        parts = args.split(maxsplit=2)
        subcmd = parts[0].lower()
        if subcmd == "add":
            if len(parts) < 2:
                print("用法：/habit add <习惯名称> [频率]")
                return
            name = parts[1]
            freq = parts[2] if len(parts) > 2 else "daily"
            habit = self.task_manager.add_habit(name, freq)
            print(f"✓ 习惯已添加 [ID: {habit.id}]")
        elif subcmd == "list":
            habits = self.task_manager.get_habits()
            if not habits:
                print("暂无习惯")
                return
            print(f"{'ID':<10} {'名称':<20} {'频率':<10} {'连续':<8} {'总计':<8}")
            print("-" * 60)
            for habit in habits:
                print(f"{habit.id:<10} {habit.title[:20]:<20} {habit.frequency:<10} {habit.streak:<8} {habit.total_completions:<8}")
        elif subcmd == "check":
            if len(parts) < 2:
                print("用法：/habit check <习惯 ID>")
                return
            if self.task_manager.habit_check_in(parts[1]):
                print("✓ 打卡成功")
            else:
                print("打卡失败（可能已打卡或 ID 不存在）")

    def _cmd_backup(self, args: str):
        """备份数据"""
        backup_name = args.strip() if args.strip() else None
        backup_path = self.data_manager.create_backup(backup_name)
        print(f"✓ 备份已创建：{backup_path}")

    def _cmd_restore(self, args: str):
        """恢复备份"""
        if not args:
            print("用法：/restore <备份名称>")
            print("可用备份:")
            for b in self.data_manager.list_backups():
                print(f"  - {b['backup_name']} ({b['created_at']})")
            return
        if self.data_manager.restore_backup(args.strip()):
            print(f"✓ 备份 {args.strip()} 已恢复")
        else:
            print(f"备份不存在：{args.strip()}")

    def _cmd_export(self, args: str):
        """导出数据"""
        if not args:
            print("用法：/export <格式>")
            print("格式：txt / excel / csv")
            return
        fmt = args.strip().lower()
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        try:
            if fmt == "txt":
                path = self.data_manager.export_to_txt(f"export_{timestamp}.txt")
            elif fmt == "excel":
                path = self.data_manager.export_to_excel(f"export_{timestamp}.xlsx")
            elif fmt == "csv":
                path = self.data_manager.export_to_csv(f"export_{timestamp}.csv")
            else:
                print(f"不支持的格式：{fmt}")
                return
            print(f"✓ 数据已导出：{path}")
        except Exception as e:
            print(f"导出失败：{e}")

    def _cmd_gui(self, args: str):
        """切换至 GUI"""
        print("正在启动图形界面...")
        self.running = False
        import subprocess
        subprocess.Popen([sys.executable, "gui.py"])

    def _cmd_exit(self, args: str):
        """退出"""
        print("再见！")
        self.running = False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Zhangy Chat R4 - CMD 模式")
    parser.add_argument('-cmd', action='store_true', help='启动 CMD 模式')
    args = parser.parse_args()

    if args.cmd:
        interface = CMDInterface()
        interface.run()
    else:
        import subprocess
        subprocess.Popen([sys.executable, "gui.py"])


if __name__ == "__main__":
    main()
