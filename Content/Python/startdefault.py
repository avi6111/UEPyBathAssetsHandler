import unreal
# 第一个测试菜单，没什么逻辑
menus = unreal.ToolMenus.get()
s = unreal.ToolMenus.get()
main_menu = menus.find_menu("LevelEditor.MainMenu")
script_menu = main_menu.add_sub_menu(
        main_menu.get_name(),"PythonTools","LightTools","Label"
)
script_menu.add_section("Test","测试")
command_string='print("ccccccccc")'
typ = unreal.ToolMenuStringCommandType.PYTHON
entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.MENU_ENTRY)
entry.set_label("测 Python 的第一个菜单")
entry.set_icon("EditorStyle","Icon.SelectInViewport")

def test():
    print("tttttttttttt")

entry.set_string_command(typ,unreal.Name("fff"),command_string)
script_menu.add_menu_entry("Test",entry)

menus.refresh_all_widgets()