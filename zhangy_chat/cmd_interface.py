#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CMD 命令行界面模块
"""

import sys
import argparse
from typing import Optional
from .task_manager import TaskManager
from .data_manager import DataManager
from .assistant import Assistant


class CMDInterface:
    """CMD 命令行界面"""
    
    def __init__(self):
        self.task_manager = TaskManager()
        self.data_manager = DataManager()
        self.assistant = Assistant()
        self.running = True
    
    def run(self):
        """运行 CMD 界面"""
        print("=" * 50)
        print("  Zhangy Chat - CMD 模式")
        print("  输入 /help 查看指令，/gui 切换图形界面，exit 退出")
        print("=" * 50)
        
        while self.running:
            try:
                cmd = input("\n> ").strip()
                if not cmd:
                    continue
                
                if cmd.startswith('/'):
                    self._handle_command(cmd)
                else:
                    # 普通对话，交给 AI 助手
                    response = self.assistant.chat(cmd)
                    print(response)
                
            except KeyboardInterrupt:
                print("\n再见！")
                break
            except Exception as e:
                print(f"错误：{e}")
    
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
            '/quit': self._cmd_exit
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
    /list [状态]                查看任务 (状态：pending/completed/all)
    /mark <ID> <状态>           标记任务状态
  
  目标规划:
    /goal add <标题> [描述]      添加目标
    /goal list                  查看目标
    /goal milestone <ID> <内容>  添加里程碑
    /review [天数]              生成复盘报告 (默认 7 天)
    /progress <ID>              查看目标进度
  
  习惯打卡:
    /habit add <名称> [频率]     添加习惯 (频率：daily/weekly)
    /habit list                 查看习惯
    /habit check <ID>           打卡
  
  数据管理:
    /backup [名称]              备份数据
    /restore <名称>             恢复备份
    /export <格式>              导出数据 (txt/excel/csv)
  
  其他:
    /gui                        切换至图形界面
    /exit                       退出程序
"""
        print(help_text)
    
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
        print(f"  标题：{task.title}")
        if description:
            print(f"  描述：{description}")
    
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
            print("状态：pending/in_progress/completed/cancelled")
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
        
        else:
            print(f"未知子指令：{subcmd}")
    
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
        if len(review['task_details']) > 5:
            print(f"   ... 还有 {len(review['task_details']) - 5} 个")
        
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
        
        else:
            print(f"未知子指令：{subcmd}")
    
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
        timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
        
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
        # 启动 GUI
        import subprocess
        subprocess.Popen([sys.executable, "gui.py"])
    
    def _cmd_exit(self, args: str):
        """退出"""
        print("再见！")
        self.running = False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Zhangy Chat - CMD 模式")
    parser.add_argument('-cmd', action='store_true', help='启动 CMD 模式')
    args = parser.parse_args()
    
    if args.cmd:
        interface = CMDInterface()
        interface.run()
    else:
        # 默认启动 GUI
        import subprocess
        subprocess.Popen([sys.executable, "gui.py"])


if __name__ == "__main__":
    main()
