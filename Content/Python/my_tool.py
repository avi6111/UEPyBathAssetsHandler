#测试 reload python
# 修改后的 my_tool.py
import unreal

def run():
    current_time = unreal.SystemLibrary.get_game_time_in_seconds(unreal.get_engine_subsystem(unreal.UnrealEditorSubsystem))
    unreal.log(f"【my_tool】这是修改后的版本！当前游戏时间：{current_time}") # 修改了这里

'''
测试，在console CMD 调用：python:
---------------------------
import importlib
import my_tool
importlib.reload(my_tool)
my_tool.run()
'''