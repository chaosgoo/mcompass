Import("env")

import subprocess

firmware_version = "1.1.0"

def get_git_info():
    try:
        # Get current branch name
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            universal_newlines=True
        ).strip()

        # Get current commit hash
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], 
            universal_newlines=True
        ).strip()

        return branch, commit
    except:
        return "unknown", "unknown"

# 读取环境变量设置型号和服务器模式
model = env.GetProjectOption("env:DEFAULT_MODEL", "GPS")  # 默认GPS
server_mode = env.GetProjectOption("env:DEFAULT_SERVER_MODE", "BLE")  # 新增服务器模式参数
model_enum = f"mcompass::Model::{model.upper()}"
server_mode_enum = f"mcompass::ServerMode::{server_mode.upper()}"  # 生成服务器模式枚举

branch, commit = get_git_info()
env.Append(CPPDEFINES=[
    ("GIT_BRANCH", '\\"%s\\"' % branch),
    ("GIT_COMMIT", '\\"%s\\"' % commit),
    ("BUILD_VERSION", '\\"%s\\"' % firmware_version),
    ("DEFAULT_MODEL", model_enum),  # 覆盖宏定义中的默认型号
    ("DEFAULT_SERVER_MODE", server_mode_enum)  # 新增服务器模式定义
])