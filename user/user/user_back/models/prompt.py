#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : prompt.py
@Time        : 2024/6/9 16:22
@Author      : Lausayick
@Email       : lausayick@foxmail.com
@Software    : PyCharm
@Function    :
@CoreLibrary :
"""


def indicator_gpu_satisfy(GPU_type='NVIDIA 3060Ti', total_memory='4096MiB', GPU_memory='115MiB', total_consumption='170W', GPU_consumption='12W', task_num=0, GPU_task_num=0, CPU_usage='12%', GPU_utilization='7%', pre_GPU_core_num=1, pre_GPU_memory='620MiB'):
    """ 新任务资源满足性指标 prompt """
    return f'''
You are a deep learning task resource satisfaction indicator scoring assistant. And I will tell you some node related information. Then, I need you to help me rate the remaining GPU resources of this node, with a partition interval of 1-100. A score of 100 indicates that it is most suitable to assign new tasks to this node:
Node GPU type:
1. The graphics card type is {GPU_type}, with a graphics memory size of {total_memory} and a maximum energy consumption of {total_consumption},
The current number of containers running on the node is {task_num}
{CPU_usage} CPU usage, {GPU_utilization} GPU utilization, 12W GPU energy {GPU_consumption}, {GPU_memory} GPU memory, and {GPU_task_num} processes using GPU,

The newly inserted task is a deep learning task, and the specific resource usage is unknown. The pre allocated GPU is {pre_GPU_core_num}vGPU, which occupies {pre_GPU_memory} of the graphics memory

Please give me a rating result and reasons as following format:
score: XXX,
reasons: XXX
'''


def indicator_task_status(total_task_num, GPU_task_num, task_status_dict):
    """ 当前节点任务进度指标 Prompt """
    return f'''
You are a task progress indicator scoring assistant for a deep learning task at the current node. I need you to judge the progress indicator of a deep learning task from multiple directions and rate it. The score range is 1-100, and a score of 100 indicates that the task is under the node, and all other tasks are about to be completed without affecting the execution of the new task.
There are a total of {total_task_num} task containers running on the current node, of which {GPU_task_num} task containers are using GPU resources. The running time and memory usage of these {GPU_task_num} tasks are as follows:
{task_status_dict}
Please rate this indicator and give me a rating result and reasons as following format:
score: XXX,
reasons: XXX
'''


def indicator_gpu_available(GPU_type='NVIDIA 3060Ti', total_memory='4096MiB', GPU_memory='115MiB', total_consumption='170W', GPU_consumption='12W', task_num=0, GPU_task_num=0, CPU_usage='12%', GPU_utilization='7%'):
    """ GPU 资源空余度指标 prompt """
    return f'''
You are a deep learning task resource satisfaction indicator scoring assistant. And I will tell you some node related information. Then, I need you to help me rate the remaining GPU resources of this node, with a partition interval of 1-100. A score of 100 indicates that the task is completely free of GPU resources at the node, which will not affect the execution of newly inserted tasks:
Node GPU type:
1. The graphics card type is {GPU_type}, with a graphics memory size of {total_memory} and a maximum energy consumption of {total_consumption},
The current number of containers running on the node is {task_num}
{CPU_usage} CPU usage, {GPU_utilization} GPU utilization, 12W GPU energy {GPU_consumption}, {GPU_memory} GPU memory, and {GPU_task_num} processes using GPU,

Please give me a rating result and reasons as following format:
score: XXX,
reasons: XXX
'''


def indicator_CPU_GPU_influence(CPU_usage_rate, memory_usage_rate, total_pod_num, GPU_usage_rate, GPU_consumption_rate, GPU_memory_usage_rate, GPU_pod_num):
    """ CPU 和 GPU 的资源联合指标 Prompt """
    return f'''
You are a joint indicator scoring assistant for CPU and GPU resources in deep learning tasks. I need you to judge the progress indicator of a deep learning task from multiple directions and rate it, with a score range of 1-100. A score of 100 indicates that the CPU resources can meet the data memory exchange with the GPU at the node, without affecting the efficiency of the GPU.
The current CPU usage rate of the node is {CPU_usage_rate}, memory usage rate is {memory_usage_rate}, and the total number of containers running on the entire node is {total_pod_num};

The current GPU usage rate of the node is {GPU_usage_rate}, GPU energy consumption accounts for {GPU_consumption_rate}, GPU memory usage is {GPU_memory_usage_rate}, and the number of GPU containers used by the entire node is {GPU_pod_num}

Please rate this indicator and give me a rating result and reasons as following format:
score: XXX,
reasons: XXX
'''


def indicator_file_space(total_file_size, model_size, data_size, pre_run_time, pre_GPU_memory, net_bandwidth):
    """ 文件资源占用 prompt """
    return f'''
You are a volume judgment assistant for deep learning tasks. I need you to judge the indicators of a deep learning task from multiple directions and rate them. The score range is 1-100, and a score of 100 indicates that the push, pull, and deployment time of the task in the current network can be ignored.
The current deep learning task has a code repository resource size of {total_file_size}, with a model size of {model_size} and a training set size of {data_size}.
The user's expected execution time is {pre_run_time} minutes, and the GPU memory usage is {pre_GPU_memory}.
The current network bandwidth is {net_bandwidth}, and there is no congestion in the network.

The influencing factors of this indicator include: file download and upload, multi-stage construction and push of Docker images, and Kubernetes' pull and deployment of images

Please rate this indicator and give me a rating result and reasons as following format:
score: XXX,
reasons: XXX
'''


if __name__ == '__main__':
    # Please add a usage instance of the package.
    pass
