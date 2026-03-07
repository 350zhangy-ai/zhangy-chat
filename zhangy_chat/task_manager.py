#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务管理模块 - 待办、目标、习惯打卡
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uuid


class Task:
    """任务类"""
    
    def __init__(self, title: str, description: str = "", priority: int = 3,
                 deadline: Optional[str] = None, tags: Optional[List[str]] = None):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.priority = priority  # 1-5, 5 最高
        self.deadline = deadline
        self.tags = tags or []
        self.status = "pending"  # pending, in_progress, completed, cancelled
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
        self.procrastination_reminder = False  # 拖延提醒
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "deadline": self.deadline,
            "tags": self.tags,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "procrastination_reminder": self.procrastination_reminder
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Task":
        task = cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", 3),
            deadline=data.get("deadline"),
            tags=data.get("tags", [])
        )
        task.id = data.get("id", task.id)
        task.status = data.get("status", "pending")
        task.created_at = data.get("created_at", task.created_at)
        task.completed_at = data.get("completed_at")
        task.procrastination_reminder = data.get("procrastination_reminder", False)
        return task


class Goal:
    """目标类"""
    
    def __init__(self, title: str, description: str = "", deadline: Optional[str] = None,
                 milestones: Optional[List[Dict]] = None):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.deadline = deadline
        self.milestones = milestones or []  # [{"title": "", "completed": false}]
        self.status = "active"  # active, completed, abandoned
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "milestones": self.milestones,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Goal":
        goal = cls(
            title=data["title"],
            description=data.get("description", ""),
            deadline=data.get("deadline"),
            milestones=data.get("milestones", [])
        )
        goal.id = data.get("id", goal.id)
        goal.status = data.get("status", "active")
        goal.created_at = data.get("created_at", goal.created_at)
        goal.completed_at = data.get("completed_at")
        return goal
    
    def get_progress(self) -> float:
        """获取目标进度百分比"""
        if not self.milestones:
            return 0.0
        completed = sum(1 for m in self.milestones if m.get("completed", False))
        return (completed / len(self.milestones)) * 100


class Habit:
    """习惯打卡类"""
    
    def __init__(self, title: str, frequency: str = "daily", 
                 target_days: Optional[List[int]] = None):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.frequency = frequency  # daily, weekly, custom
        self.target_days = target_days or list(range(7))  # 0=Monday, 6=Sunday
        self.check_ins = []  # [{"date": "YYYY-MM-DD", "completed": true}]
        self.created_at = datetime.now().isoformat()
        self.streak = 0  # 连续打卡天数
        self.total_completions = 0
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "frequency": self.frequency,
            "target_days": self.target_days,
            "check_ins": self.check_ins,
            "created_at": self.created_at,
            "streak": self.streak,
            "total_completions": self.total_completions
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Habit":
        habit = cls(
            title=data["title"],
            frequency=data.get("frequency", "daily"),
            target_days=data.get("target_days")
        )
        habit.id = data.get("id", habit.id)
        habit.check_ins = data.get("check_ins", [])
        habit.created_at = data.get("created_at", habit.created_at)
        habit.streak = data.get("streak", 0)
        habit.total_completions = data.get("total_completions", 0)
        return habit
    
    def check_in(self, date: Optional[str] = None) -> bool:
        """打卡"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 检查是否已打卡
        for check_in in self.check_ins:
            if check_in["date"] == date:
                return False
        
        self.check_ins.append({"date": date, "completed": True})
        self.total_completions += 1
        self._update_streak()
        return True
    
    def _update_streak(self):
        """更新连续打卡天数"""
        today = datetime.now().date()
        dates = sorted([datetime.fromisoformat(ci["date"]).date() 
                       for ci in self.check_ins], reverse=True)
        
        streak = 0
        for i, date in enumerate(dates):
            if i == 0:
                if date == today:
                    streak = 1
                elif date == today - timedelta(days=1):
                    streak = 1
                else:
                    break
            else:
                if date == dates[i-1] - timedelta(days=1):
                    streak += 1
                else:
                    break
        self.streak = streak


class TaskManager:
    """任务管理器"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.tasks_file = self.data_dir / "tasks.json"
        self.goals_file = self.data_dir / "goals.json"
        self.habits_file = self.data_dir / "habits.json"
        
        self.tasks: List[Task] = []
        self.goals: List[Goal] = []
        self.habits: List[Habit] = []
        
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in tasks_data]
        
        if self.goals_file.exists():
            with open(self.goals_file, 'r', encoding='utf-8') as f:
                goals_data = json.load(f)
                self.goals = [Goal.from_dict(g) for g in goals_data]
        
        if self.habits_file.exists():
            with open(self.habits_file, 'r', encoding='utf-8') as f:
                habits_data = json.load(f)
                self.habits = [Habit.from_dict(h) for h in habits_data]
    
    def _save_data(self):
        """保存数据"""
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in self.tasks], f, ensure_ascii=False, indent=2)
        
        with open(self.goals_file, 'w', encoding='utf-8') as f:
            json.dump([g.to_dict() for g in self.goals], f, ensure_ascii=False, indent=2)
        
        with open(self.habits_file, 'w', encoding='utf-8') as f:
            json.dump([h.to_dict() for h in self.habits], f, ensure_ascii=False, indent=2)
    
    # 任务管理方法
    def add_task(self, title: str, description: str = "", priority: int = 3,
                 deadline: Optional[str] = None, tags: Optional[List[str]] = None) -> Task:
        """添加任务"""
        task = Task(title, description, priority, deadline, tags)
        self.tasks.append(task)
        self._save_data()
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                self._save_data()
                return True
        return False
    
    def update_task_status(self, task_id: str, status: str) -> bool:
        """更新任务状态"""
        for task in self.tasks:
            if task.id == task_id:
                task.status = status
                if status == "completed":
                    task.completed_at = datetime.now().isoformat()
                self._save_data()
                return True
        return False
    
    def get_tasks(self, status: Optional[str] = None, 
                  priority: Optional[int] = None) -> List[Task]:
        """获取任务列表"""
        result = self.tasks
        if status:
            result = [t for t in result if t.status == status]
        if priority:
            result = [t for t in result if t.priority == priority]
        return sorted(result, key=lambda x: (-x.priority, x.created_at))
    
    def get_procrastination_tasks(self) -> List[Task]:
        """获取需要拖延提醒的任务"""
        now = datetime.now()
        result = []
        for task in self.tasks:
            if task.status == "pending" and task.deadline:
                deadline = datetime.fromisoformat(task.deadline)
                if (deadline - now).total_seconds() < 3600:  # 1 小时内到期
                    result.append(task)
        return result
    
    # 目标管理方法
    def add_goal(self, title: str, description: str = "", 
                 deadline: Optional[str] = None,
                 milestones: Optional[List[Dict]] = None) -> Goal:
        """添加目标"""
        goal = Goal(title, description, deadline, milestones)
        self.goals.append(goal)
        self._save_data()
        return goal
    
    def delete_goal(self, goal_id: str) -> bool:
        """删除目标"""
        for i, goal in enumerate(self.goals):
            if goal.id == goal_id:
                self.goals.pop(i)
                self._save_data()
                return True
        return False
    
    def update_goal_status(self, goal_id: str, status: str) -> bool:
        """更新目标状态"""
        for goal in self.goals:
            if goal.id == goal_id:
                goal.status = status
                if status == "completed":
                    goal.completed_at = datetime.now().isoformat()
                self._save_data()
                return True
        return False
    
    def add_milestone(self, goal_id: str, milestone_title: str) -> bool:
        """添加里程碑"""
        for goal in self.goals:
            if goal.id == goal_id:
                goal.milestones.append({
                    "title": milestone_title,
                    "completed": False,
                    "created_at": datetime.now().isoformat()
                })
                self._save_data()
                return True
        return False
    
    def complete_milestone(self, goal_id: str, milestone_index: int) -> bool:
        """完成里程碑"""
        for goal in self.goals:
            if goal.id == goal_id:
                if 0 <= milestone_index < len(goal.milestones):
                    goal.milestones[milestone_index]["completed"] = True
                    self._save_data()
                    return True
        return False
    
    def get_goals(self, status: Optional[str] = None) -> List[Goal]:
        """获取目标列表"""
        if status:
            return [g for g in self.goals if g.status == status]
        return self.goals
    
    def get_goal_progress(self, goal_id: str) -> Optional[float]:
        """获取目标进度"""
        for goal in self.goals:
            if goal.id == goal_id:
                return goal.get_progress()
        return None
    
    # 习惯管理方法
    def add_habit(self, title: str, frequency: str = "daily",
                  target_days: Optional[List[int]] = None) -> Habit:
        """添加习惯"""
        habit = Habit(title, frequency, target_days)
        self.habits.append(habit)
        self._save_data()
        return habit
    
    def delete_habit(self, habit_id: str) -> bool:
        """删除习惯"""
        for i, habit in enumerate(self.habits):
            if habit.id == habit_id:
                self.habits.pop(i)
                self._save_data()
                return True
        return False
    
    def habit_check_in(self, habit_id: str, date: Optional[str] = None) -> bool:
        """习惯打卡"""
        for habit in self.habits:
            if habit.id == habit_id:
                return habit.check_in(date)
        return False
    
    def get_habits(self) -> List[Habit]:
        """获取习惯列表"""
        return self.habits
    
    def get_habit_stats(self, habit_id: str) -> Optional[Dict]:
        """获取习惯统计"""
        for habit in self.habits:
            if habit.id == habit_id:
                return {
                    "streak": habit.streak,
                    "total_completions": habit.total_completions,
                    "frequency": habit.frequency
                }
        return None
    
    # 复盘报告
    def generate_review(self, days: int = 7) -> Dict:
        """生成阶段性复盘报告"""
        now = datetime.now()
        start_date = now - timedelta(days=days)
        
        completed_tasks = [t for t in self.tasks 
                         if t.status == "completed" and t.completed_at
                         and datetime.fromisoformat(t.completed_at).date() >= start_date.date()]
        
        active_goals = [g for g in self.goals if g.status == "active"]
        
        return {
            "period": f"{start_date.strftime('%Y-%m-%d')} 至 {now.strftime('%Y-%m-%d')}",
            "completed_tasks": len(completed_tasks),
            "task_details": [t.to_dict() for t in completed_tasks],
            "active_goals": len(active_goals),
            "goal_progress": [{"title": g.title, "progress": g.get_progress()} 
                            for g in active_goals],
            "habits_summary": [{"title": h.title, "streak": h.streak, 
                              "total": h.total_completions} for h in self.habits]
        }
