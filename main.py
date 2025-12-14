# -*- coding: utf-8 -*-
"""
智能自适应打砖块游戏 - 主程序入口
作者: xzh
功能: 提供游戏菜单，支持经典模式和挑战模式，记录游戏数据并生成报告
"""

import sys
from config import *
from game import Game_xzh, save_game_data_xzh
from analytics import generate_player_report_xzh, print_statistics_xzh


def display_menu_xzh():
    """显示主菜单"""
    print("\n" + "="*50)
    print("智能自适应打砖块游戏".center(50))
    print("="*50)
    print("\n请选择选项:")
    print("1. 经典模式 (Classic Mode)")
    print("2. 挑战模式 (Challenge Mode)")
    print("3. 查看统计数据")
    print("4. 生成能力报告")
    print("5. 退出游戏")
    print("-"*50)


def get_user_choice_xzh():
    """
    获取用户选择
    :return: 用户选择的选项
    """
    while True:
        try:
            choice = input("请输入选项 (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("无效选项，请重新输入！")
        except Exception as e:
            print(f"输入错误: {e}")


def start_game_xzh(mode):
    """
    启动游戏
    :param mode: 游戏模式
    """
    try:
        print(f"\n启动{'经典' if mode == MODE_CLASSIC_XZH else '挑战'}模式...")
        print("\n游戏操作说明:")
        print("- 使用左右方向键或 A/D 键移动挡板")
        print("- 按空格键发射球")
        print("- 按 ESC 键退出游戏")
        print("\n游戏即将开始...\n")

        # 创建并运行游戏
        game = Game_xzh(mode)
        game_data = game.run_xzh()

        # 保存游戏数据
        if game_data and game_data.get('score', 0) > 0:
            save_game_data_xzh(game_data)
            print("\n游戏结束!")
            print(f"得分: {game_data['score']}")
            print(f"命中率: {game_data['hit_rate']*100:.2f}%")
            print(f"游戏时长: {game_data['duration']:.1f} 秒")
            if game_data.get('won', False):
                print("恭喜你获胜！")
            else:
                print("继续努力！")

    except Exception as e:
        print(f"游戏运行错误: {e}")
        import traceback
        traceback.print_exc()


def view_statistics_xzh():
    """查看统计数据"""
    try:
        print_statistics_xzh()
        input("\n按回车键返回主菜单...")
    except Exception as e:
        print(f"查看统计数据错误: {e}")


def generate_report_xzh():
    """生成能力报告"""
    try:
        print("\n正在生成玩家能力报告...")
        generate_player_report_xzh()
        input("\n按回车键返回主菜单...")
    except Exception as e:
        print(f"生成报告错误: {e}")


def main_xzh():
    """主函数"""
    print("\n欢迎来到智能自适应打砖块游戏！")

    while True:
        try:
            display_menu_xzh()
            choice = get_user_choice_xzh()

            if choice == '1':
                # 经典模式
                start_game_xzh(MODE_CLASSIC_XZH)
            elif choice == '2':
                # 挑战模式
                start_game_xzh(MODE_CHALLENGE_XZH)
            elif choice == '3':
                # 查看统计数据
                view_statistics_xzh()
            elif choice == '4':
                # 生成能力报告
                generate_report_xzh()
            elif choice == '5':
                # 退出游戏
                print("\n感谢游玩，再见！")
                sys.exit(0)

        except KeyboardInterrupt:
            print("\n\n游戏被中断，再见！")
            sys.exit(0)
        except Exception as e:
            print(f"\n程序错误: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main_xzh()
