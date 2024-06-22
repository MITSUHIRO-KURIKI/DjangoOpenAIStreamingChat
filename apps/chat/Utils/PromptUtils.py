from django.conf import settings
from common.scripts.PythonCodeUtils import print_color

def NextQuestionAssistantPrompt(user_sentence:str,
                                llm_response:str,
                                history_text:list,
                                ) -> str:
    # Verify the input is valid.
    if not user_sentence:
        raise ValueError('Please set user_sentence.')
    if not llm_response:
        raise ValueError('Please set llm_response.')

    prompt = f"""以下の HUMAN と ASSISTANT AI の会話で、 HUMAN が次に質問しそうな内容（質問する文章）を、４つ書き出してください。必ず # 出力形式 に記載の Python の JSON形式 で出力しなさい。

{history_text}
## HUMAN (Now)
````
{user_sentence}
````

## ASSISTANT AI (Now)
````
{llm_response}
````

## 禁止事項
丁寧な表現は禁止する。
以下の出力形式以外の出力を禁止する。

## 出力形式
必ずPythonのJSON形式で出力しなさい。
例:
```python
{{
    "NextHumanQuestionsList": [
        "A",
        "B",
        "C",
        "D"
    ]
}}
```
"""
    if settings.DEBUG:
        print_color(f'NextQuestionAssistantPrompt:\n{prompt}', 4)

    return prompt
