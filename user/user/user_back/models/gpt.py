#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : gpt.py
@Time        : 2024/6/9 17:13
@Author      : Lausayick
@Email       : lausayick@foxmail.com
@Software    : PyCharm
@Function    :
@CoreLibrary :
"""
import openai
API_KEY = ''


def get_gpt_response(model_ext='gpt-4o', temp=0.0, max_tk=16, top_p=0, frequency_penalty=0, presence_penalty=0,
                     response_format={"type": "text"}, system_text='You are a deep learning task assistant.', input_text=''):
    """ 获取 GPT 返回结果 """
    openai_client = openai.OpenAI(api_key=API_KEY)
    try:
        response = openai_client.chat.completions.create(
            model=model_ext,
            temperature=temp,
            max_tokens=max_tk,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            response_format=response_format,
            messages=[
                {"role": "system", "content": system_text},
                {"role": "user", "content": input_text}
            ]
            ,
        )
        result = response.choices[0].message.content
    except Exception:
        result = 'Error When Connect With GPT.'

    return result


if __name__ == '__main__':
    # Please add a usage instance of the package.
    pass
