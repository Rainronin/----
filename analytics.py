# -*- coding: utf-8 -*-
"""
数据分析和可视化模块
使用Matplotlib生成玩家能力报告图
"""

import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
from config import *
from game import load_game_data_xzh

# 设置中文字体（防止中文显示为方块）
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


def generate_player_report_xzh():
    """生成玩家能力报告图表"""
    try:
        # 加载游戏数据
        games = load_game_data_xzh()

        if not games:
            print("没有游戏数据，无法生成报告")
            return

        print(f"找到 {len(games)} 局游戏记录")

        # 创建图表
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Player Performance Report', fontsize=16, fontweight='bold')

        # 1. 分数趋势图
        plot_score_trend_xzh(axes[0, 0], games)

        # 2. 命中率趋势图
        plot_hit_rate_trend_xzh(axes[0, 1], games)

        # 3. 游戏时长分布图
        plot_duration_distribution_xzh(axes[1, 0], games)

        # 4. 模式对比图
        plot_mode_comparison_xzh(axes[1, 1], games)

        # 调整布局
        plt.tight_layout()

        # 保存图表
        plt.savefig(REPORT_IMAGE_PATH_XZH, dpi=300, bbox_inches='tight')
        print(f"报告已保存到 {REPORT_IMAGE_PATH_XZH}")

        # 显示图表
        plt.show()

    except Exception as e:
        print(f"生成报告错误: {e}")


def plot_score_trend_xzh(ax, games):
    """
    绘制分数趋势图
    :param ax: matplotlib axes对象
    :param games: 游戏数据列表
    """
    scores = [game['score'] for game in games]
    game_numbers = list(range(1, len(scores) + 1))

    ax.plot(game_numbers, scores, marker='o', linestyle='-', linewidth=2,
            markersize=6, color='#2E86DE', label='Score')

    # 添加平均线
    if scores:
        avg_score = sum(scores) / len(scores)
        ax.axhline(y=avg_score, color='red', linestyle='--',
                   label=f'Average: {avg_score:.0f}')

    ax.set_xlabel('Game Number', fontsize=12)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Score Trend', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)


def plot_hit_rate_trend_xzh(ax, games):
    """
    绘制命中率趋势图
    :param ax: matplotlib axes对象
    :param games: 游戏数据列表
    """
    hit_rates = [game['hit_rate'] * 100 for game in games]
    game_numbers = list(range(1, len(hit_rates) + 1))

    ax.plot(game_numbers, hit_rates, marker='s', linestyle='-', linewidth=2,
            markersize=6, color='#10AC84', label='Hit Rate')

    # 添加平均线
    if hit_rates:
        avg_hit_rate = sum(hit_rates) / len(hit_rates)
        ax.axhline(y=avg_hit_rate, color='orange', linestyle='--',
                   label=f'Average: {avg_hit_rate:.1f}%')

    ax.set_xlabel('Game Number', fontsize=12)
    ax.set_ylabel('Hit Rate (%)', fontsize=12)
    ax.set_title('Hit Rate Trend', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.legend()
    ax.grid(True, alpha=0.3)


def plot_duration_distribution_xzh(ax, games):
    """
    绘制游戏时长分布图
    :param ax: matplotlib axes对象
    :param games: 游戏数据列表
    """
    durations = [game['duration'] / 60 for game in games]  # 转换为分钟

    if durations:
        ax.hist(durations, bins=10, color='#A55EEA', alpha=0.7, edgecolor='black')
        ax.set_xlabel('Duration (minutes)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Game Duration Distribution', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        # 添加统计信息
        avg_duration = sum(durations) / len(durations)
        ax.axvline(x=avg_duration, color='red', linestyle='--',
                   label=f'Average: {avg_duration:.1f} min')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14)


def plot_mode_comparison_xzh(ax, games):
    """
    绘制模式对比图
    :param ax: matplotlib axes对象
    :param games: 游戏数据列表
    """
    # 统计各模式数据
    classic_games = [g for g in games if g['mode'] == MODE_CLASSIC_XZH]
    challenge_games = [g for g in games if g['mode'] == MODE_CHALLENGE_XZH]

    modes = []
    avg_scores = []
    avg_hit_rates = []

    if classic_games:
        modes.append('Classic')
        avg_scores.append(sum(g['score'] for g in classic_games) / len(classic_games))
        avg_hit_rates.append(sum(g['hit_rate'] for g in classic_games) / len(classic_games) * 100)

    if challenge_games:
        modes.append('Challenge')
        avg_scores.append(sum(g['score'] for g in challenge_games) / len(challenge_games))
        avg_hit_rates.append(sum(g['hit_rate'] for g in challenge_games) / len(challenge_games) * 100)

    if modes:
        x = range(len(modes))
        width = 0.35

        bars1 = ax.bar([i - width/2 for i in x], avg_scores, width,
                       label='Avg Score', color='#FC5C65')

        # 创建第二个Y轴
        ax2 = ax.twinx()
        bars2 = ax2.bar([i + width/2 for i in x], avg_hit_rates, width,
                        label='Avg Hit Rate (%)', color='#45AAF2')

        ax.set_xlabel('Game Mode', fontsize=12)
        ax.set_ylabel('Average Score', fontsize=12, color='#FC5C65')
        ax2.set_ylabel('Average Hit Rate (%)', fontsize=12, color='#45AAF2')
        ax.set_title('Mode Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(modes)

        # 合并图例
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

        ax.tick_params(axis='y', labelcolor='#FC5C65')
        ax2.tick_params(axis='y', labelcolor='#45AAF2')
    else:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14)


def print_statistics_xzh():
    """打印游戏统计信息"""
    try:
        games = load_game_data_xzh()

        if not games:
            print("没有游戏数据")
            return

        print("\n" + "="*50)
        print("游戏统计信息".center(50))
        print("="*50)

        # 总体统计
        total_games = len(games)
        total_score = sum(g['score'] for g in games)
        avg_score = total_score / total_games if total_games > 0 else 0
        max_score = max(g['score'] for g in games) if games else 0
        wins = sum(1 for g in games if g.get('won', False))

        print(f"\n总游戏局数: {total_games}")
        print(f"总得分: {total_score}")
        print(f"平均分: {avg_score:.2f}")
        print(f"最高分: {max_score}")
        print(f"胜利次数: {wins} ({wins/total_games*100:.1f}%)" if total_games > 0 else "胜利次数: 0")

        # 命中率统计
        avg_hit_rate = sum(g['hit_rate'] for g in games) / total_games if total_games > 0 else 0
        print(f"平均命中率: {avg_hit_rate*100:.2f}%")

        # 模式统计
        classic_count = sum(1 for g in games if g['mode'] == MODE_CLASSIC_XZH)
        challenge_count = sum(1 for g in games if g['mode'] == MODE_CHALLENGE_XZH)
        print(f"\n经典模式: {classic_count} 局")
        print(f"挑战模式: {challenge_count} 局")

        # 最近5局
        if total_games > 0:
            print("\n最近5局记录:")
            print("-" * 50)
            recent_games = games[-5:]
            for i, game in enumerate(reversed(recent_games), 1):
                status = "胜利" if game.get('won', False) else "失败"
                print(f"{i}. [{game['mode']}] 分数: {game['score']}, "
                      f"命中率: {game['hit_rate']*100:.1f}%, "
                      f"状态: {status}, "
                      f"时间: {game['timestamp']}")

        print("="*50 + "\n")

    except Exception as e:
        print(f"打印统计信息错误: {e}")


if __name__ == "__main__":
    # 测试功能
    print_statistics_xzh()
    generate_player_report_xzh()
