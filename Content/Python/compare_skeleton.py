#写python api参考✅：https://blog.csdn.net/kuangben2000/article/details/142438915
import unreal
class HashableBoneNode:
    """可哈希的BoneNode封装类"""
    def __init__(self, control_rig, node_id):
        self.control_rig = control_rig
        self.node_id = node_id
        #self.bone_node = control_rig.get_node(node_id)
        # 预存常用属性
        #self.node_name = control_rig.get_node_title(node_id)
        #self.bone_name = self.bone_node.get_property("Bone") if self.bone_node else ""
        self.node_name = 'node__'
        self.bone_name = 'temp'
    
    # 实现哈希方法（基于唯一的node_id）
    def __hash__(self):
        return hash(self.node_id)
    
    # 实现相等判断
    def __eq__(self, other):
        if not isinstance(other, HashableBoneNode):
            return False
        return self.node_id == other.node_id
    
    def __repr__(self):
        return f"HashableBoneNode(name={self.node_name}, bone={self.bone_name})"
    
#一开始是AI的代码，但是一段代码要“人手”从头换到尾，也是不容易。。。。
def compare_skeleton_bones(src_skel_path, dst_skel_path):
    """
    对比两个骨架资产的骨骼名称列表。
    :param src_skel_path: 源骨架资产路径（例如 "/Game/Characters/Master_Skeleton.Master_Skeleton"）
    :param dst_skel_path: 目标骨架资产路径（例如 "/Game/Characters/Armor_Skeleton.Armor_Skeleton"）
    """
    # 加载资产
    src_skel = unreal.EditorAssetLibrary.load_asset(src_skel_path)
    dst_skel = unreal.EditorAssetLibrary.load_asset(dst_skel_path)

    if not src_skel or not dst_skel:
        unreal.log_error("无法加载骨架资产，请检查路径。")
        return False
    #获取 LogPython: <Object '/Game/Ani/PillawAutoRig_Skeleton1.PillawAutoRig_Skeleton1' (0x00000000A7CF6400) Class 'Skeleton'>
    print(src_skel)
    # AttributeError: 'AnimPose' object has no attribute 'get_num_bones'
    # ✅ 正确方式：通过 get_reference_pose 获取骨骼信息
    src_pose = src_skel.get_reference_pose()# ❌获取的是 AnimPos (??后来发现这个对象有 .get_bone_names()???)
    dst_pose = dst_skel.get_reference_pose()
    # 获取骨骼数量
    #src_bone_num = src_pose.get_num_bones()# ❌没有的
    #dst_bone_num = dst_pose.get_num_bones()
    #print('[num=]',src_bone_num)
    # ❔ 打印所有可访问的属性和方法
    print(dir(src_skel))# ♾️dir 应该是 python 的高级写法 

    # 2. ❔打印所有Editor属性（编辑器专属）（本可以打印前 ✅30 个）
    # print("\n2. Editor属性列表（前30个）:")
    # all_properties = unreal.EditorReflectionLibrary.get_properties_for_class(src_skel)# 获取所有属性（包括运行时和编辑器属性）# ❌
    # for idx, attr in enumerate(all_properties[:30]):
    #     print(f"   {idx+1}. {attr}")

    # ❔ ，找到一个可以调用的方法；然并卵；LogPython: 发现方法: get_editor_property
    all_members = dir(src_skel)
    found_count = 0
    for member_name in all_members:
        if member_name.startswith('get_editor_property'):
            # 尝试获取该方法
            method = getattr(src_skel, member_name, None)
            if callable(method):
                print(f"发现方法: {member_name}()")
                found_count += 1
    #print(src_skel.get)
    
    # ✅
    print('skeleton:',src_pose.get_bone_names())
    # ✅ https://forums.unrealengine.com/t/ue-5-5-using-python-or-a-blueprint-is-there-a-way-to-see-if-a-joint-name-exists-in-a-skeleton/2525282/3

    dst_bones = dst_skel.get_editor_property('bone_tree')
    src_bones = src_skel.get_editor_property('bone_tree')
    bone_tree = src_bones
    print(bone_tree)
    for x in bone_tree:
        print(x)

    #print(src_skel.reference_skeleton)# ❌
    # # ❌ 方式：通过 get_editor_property 获取 reference_skeleton
    # src_ref_skeleton = src_skel.get_editor_property('reference_skeleton')
    # dst_ref_skeleton = dst_skel.get_editor_property('reference_skeleton')
    # print(src_ref_skeleton)

    ## ❌获取骨骼名称列表
    #src_bones = [bone.name for bone in src_skel.get_editor_property('reference_skeleton').get_raw_bone_data()]
    #dst_bones = [bone.name for bone in dst_skel.get_editor_property('reference_skeleton').get_raw_bone_data()]
    # ❌ 获取骨骼名称列表
    #src_bones = [bone.name for bone in src_ref_skeleton.get_raw_bone_data()]
    #dst_bones = [bone.name for bone in dst_ref_skeleton.get_raw_bone_data()]

    # ❌主逻辑：找出差异(本身字典处理（AI逻辑）是好的，非常好的逻辑，只是。。。。。总之就是 1/10 的逻辑都没有了，要改掉)
    # 一些个经典写法（存在教科书多年，现在被AI使用）
    # 但其实根据本人多年经验，很多经典写法，在实际应用中（各种原因,甚至是程序员不成熟，团队不成熟的原因），先不考虑这些原因
    # 即使不考虑这些原因，比较理想的开发环境下，这些经典写法，能占实际应用的比例甚至不到 1/8
    # 一个app store里面有8个音乐APP，只有不到1个APP会用这种经典写法
    # 大部分 pp 其实都是各种“狮山”代码，但你吐槽他“狮山”实际可能非常好用
    # 经典之所以成为经典，和现实（硬件）条件不一样，
    # 常用，好用的写法是实战中好用的流传写法（可能并不科学）绝对不是教科书里的工整的，经典写法
    # 这是教科书写法，但实际上类似于（偏方，传统菜谱）这种写法才是比较靠谱的写法
    # （同法律一样，绝对的原教旨主义不存在的）这也是软件同硬件的不同
    # missing_in_dst = set(src_bones) - set(dst_bones)
    # extra_in_dst = set(dst_bones) - set(src_bones)
    
    # 之前测试/错误代码---------------
    src_names = []
    dst_names = []
    hashID = 0;
    for x in bone_tree:
        #print(dir(x))
        #src_names.append(x)
        #print(x.export_text())#LogPython: (TranslationRetargetingMode=Animation)
        #print(x.__doc__)#Source: C++ .... Editor Properties:等"✅
        #print(x.__getattribute__("bone_name"))# ❌
        #print(x.get_editor_property("translation_retargeting_mode")) #OK
        #print(x.__getstate__()) #完全为 None
        src_names.append(HashableBoneNode(x,hashID))
        hashID=hashID+1
    for y in dst_bones:
        dst_names.append(y)

    # Fixed ---------------------------------
    src_names = src_pose.get_bone_names()
    dst_names = dst_pose.get_bone_names()
    missing_in_dst = set(src_names) - set(dst_names)
    extra_in_dst = set(dst_names) - set(src_names)

    unreal.log("=" * 50)
    unreal.log(f"源骨架 ({src_skel_path}) 骨骼数量: {len(src_bones)}")
    unreal.log(f"目标骨架 ({dst_skel_path}) 骨骼数量: {len(dst_bones)}")

    if missing_in_dst:
        #printStr ='\n'.join(map(str,sorted(list(missing_in_dst))))#暂时不需要排序
        printStr ='\n'.join(map(str,list(missing_in_dst)))
        unreal.log_warning(f"目标骨架中缺失的骨骼: {printStr}",)
    else:
        unreal.log("✅ 目标骨架没有缺失骨骼。")

    print('----------------------->')
    if extra_in_dst:
        printStr = "\n".join(map(str,list(extra_in_dst)))
        unreal.log_warning(f"目标骨架中多余的骨骼: {printStr}")
    else:
        unreal.log("✅ 目标骨架没有多余骨骼。")
    unreal.log("=" * 50)

    #return len(missing_in_dst) == 0


#这个方法，一开始AI还写了备注，是一个错的备注（已删除）
compare_skeleton_bones(
    "/Game/Ani/PillawAutoRig_Skeleton1.PillawAutoRig_Skeleton1",
    "/Game/Characters/Mannequins/Meshes/SK_Mannequin.SK_Mannequin"
)

'''测试代码：
import importlib
import compare_skeleton
importlib.reload(compare_skeleton)
'''

'''参考库
https://github.com/Tangerie/Json2DA/blob/master/utils.py
https://github.com/20tab/UnrealEnginePython/blob/master/tutorials/SnippetsForStaticAndSkeletalMeshes.md
https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/?application_version=5.7

'''