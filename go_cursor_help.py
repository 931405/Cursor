import platform
import os
import subprocess
import sys
import ctypes
from logger import logging
from language import get_translation

def is_admin():
    """检查是否具有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员权限重新运行脚本"""
    try:
        if sys.argv[0].endswith('.py'):
            args = [sys.executable] + sys.argv
        else:
            args = sys.argv
        
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            args[0],
            ' '.join(args[1:]), 
            None, 
            1
        )
        return True
    except Exception as e:
        logging.error(f"提升权限失败: {str(e)}")
        return False

def go_cursor_help():
    system = platform.system()
    logging.info(get_translation("current_operating_system", system=system))
    
    base_url = "https://aizaozao.com/accelerate.php/https://raw.githubusercontent.com/yuaotian/go-cursor-help/refs/heads/master/scripts/run"
    
    if system == "Darwin":  # macOS
        cmd = f'curl -k -fsSL {base_url}/cursor_mac_id_modifier.sh | sudo bash'
        logging.info(get_translation("executing_macos_command"))
        os.system(cmd)
    elif system == "Linux":
        cmd = f'curl -fsSL {base_url}/cursor_linux_id_modifier.sh | sudo bash'
        logging.info(get_translation("executing_linux_command"))
        os.system(cmd)
    elif system == "Windows":
        if not is_admin():
            logging.warning("需要管理员权限，正在尝试提升权限...")
            if run_as_admin():
                sys.exit(0)  # 成功启动新进程后退出当前进程
            else:
                logging.error("请右键点击脚本，选择'以管理员身份运行'")
                input("按回车键退出...")
                sys.exit(1)
        
        cmd = f'irm {base_url}/cursor_win_id_modifier.ps1 | iex'
        logging.info(get_translation("executing_windows_command"))
        try:
            # 使用管理员权限执行PowerShell命令
            process = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
                capture_output=True,
                text=True,
                shell=True
            )
            if process.returncode != 0:
                logging.error(f"命令执行失败: {process.stderr}")
                return False
            logging.info(process.stdout)
        except Exception as e:
            logging.error(f"执行命令时出错: {str(e)}")
            return False
    else:
        logging.error(get_translation("unsupported_operating_system", system=system))
        return False
    
    return True

def main():
    go_cursor_help()

if __name__ == "__main__":
    main()