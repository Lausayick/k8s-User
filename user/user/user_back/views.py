from django.shortcuts import render
from django.http import JsonResponse
import time
import random
import subprocess
import os


def get_cmd_response(command: list):
    """ 执行CMD命令并且获取输出 """
    try:
        # 执行命令并获取输出
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，则打印错误信息并返回 None
        print("Error:", e)
        return None


def handle_gpu_info(GPU_info):
    """ 解析 GPU 参数文本 """
    # 拆分行
    lines = GPU_info.split('\n')

    # 初始化结果字典
    result = {
        "Driver Version": None,
        "CUDA Version": None,
        "GPU Name": None,
        "Bus-Id": None,
        "Disp.A": None,
        "Volatile Uncorr. ECC": None,
        "Fan": None,
        "Temp": None,
        "Perf": None,
        "Pwr Usage/Cap": None,
        "Memory-Usage": None,
        "GPU-Util": None,
        "Compute M.": None,
        "MIG M.": None,
        "任务进程总数": 0,
        "任务进程信息": []
    }

    # 解析基本信息
    for line in lines:
        if 'Driver Version:' in line and 'CUDA Version:' in line:
            parts = line.split('|')
            driver_info = parts[1].split()
            result["Driver Version"] = driver_info[1]
            result["CUDA Version"] = driver_info[7]

        if 'GPU  Name' in line:
            parts = line.split('|')
            result["GPU Name"] = parts[1].split()[2:]

        if 'N/A   ' in line:
            parts = line.split('|')
            result["Bus-Id"] = parts[2].strip().split()[0]
            result["Disp.A"] = parts[2].strip().split()[1]
            result["Volatile Uncorr. ECC"] = parts[2].strip().split()[2]
            result["Fan"] = parts[1].strip().split()[0]
            result["Temp"] = parts[1].strip().split()[1]
            result["Perf"] = parts[1].strip().split()[2]
            result["Pwr Usage/Cap"] = parts[1].strip().split()[3]
            result["Memory-Usage"] = parts[2].strip().split()[0]
            result["GPU-Util"] = parts[2].strip().split()[1]
            result["Compute M."] = parts[2].strip().split()[2]
            # result["MIG M."] = parts[2].strip().split()[3]

    # 解析任务进程信息
    process_section = False
    for line in lines:
        if 'Processes:' in line:
            process_section = True
            continue
        if process_section:
            if '|' in line:
                process_info = line.split('|')
                if len(process_info) > 2:
                    process_data = process_info[2].strip().split()
                    if len(process_data) >= 6:
                        pid = process_data[2]
                        process_name = process_data[5]
                        mem_usage = process_data[-2]
                        process_dict = {
                            "PID": pid,
                            "Process name": process_name,
                            "GPU Memory Usage": mem_usage
                        }
                        result["任务进程信息"].append(process_dict)

    # 计算任务进程总数
    result["任务进程总数"] = len(result["任务进程信息"])

    return result


def handle_cpu_info(CPU_info):
    """ 解析 CPU 信息 """
    # 拆分行
    lines = CPU_info.strip().split('\n')

    # 解析表头
    headers = lines[0].split()

    # 初始化结果字典
    result = {}

    # 解析每个节点的信息
    for line in lines[1:]:
        values = line.split()
        node_dict = {headers[i]: values[i] for i in range(len(headers))}
        result[values[0]] = node_dict

    return result


# Create your views here.
def getEnvironment(request):
    """ 获取环境参数 """
    docker_version = get_cmd_response(command=["docker version"])
    kubectl_version = get_cmd_response(command=["kubectl version"])
    result = {
        "docker": docker_version,
        "kubectl": kubectl_version
    }
    return JsonResponse(result)


def installEnvironment(request):
    """ 创建环境部署 """
    return JsonResponse({})


def getMetricInfo(request):
    """ 读取监控数据 """
    resource_type = request.POST.get("resource_type")
    if resource_type == '' or resource_type is None:
        return JsonResponse({"error": "错误输入"})
    # 分类读取
    if resource_type == 'GPU':
        GPU_info = get_cmd_response(["nvidia-smi"])
        result = handle_gpu_info(GPU_info=GPU_info)

    elif resource_type == 'CPU':
        CPU_info = get_cmd_response(["kubectl top nodes"])
        result = handle_cpu_info(CPU_info=CPU_info)

    else:
        result = {}

    return JsonResponse(result)


def createNewTask(request):
    """ 插入新任务 """
    # 读取用户输入参数
    files = request.FILES.get("Task_File")
    filename = os.path.join(os.path.basename(__file__), files.name)
    file_size = files.size()
    with open(filename, 'wb') as f:
        f.write(files.read())

    # 测试任务参数

    # 计算策略指标

    # 生成Docker镜像

    # 生成Kubernetes文件

    return JsonResponse({})


def migrateTask(request):
    """ 任务迁移 """
    # 单
    return JsonResponse({})
