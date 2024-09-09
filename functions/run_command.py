import subprocess

def run_command(command: str):
    try:
        # 使用 subprocess.run 捕获输出和错误
        result = subprocess.run(command, shell=True, check=True, 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 返回命令的输出、错误信息和退出码
        return {
            'stdout': result.stdout,    # 标准输出
            'stderr': result.stderr,    # 标准错误
            'returncode': result.returncode  # 退出状态码
        }

    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，返回错误输出和状态码
        return {
            'stdout': e.stdout,
            'stderr': e.stderr,
            'returncode': e.returncode
        }
