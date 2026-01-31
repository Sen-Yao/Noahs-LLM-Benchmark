# Noah's LLM Benchmark

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

个人使用的大语言模型（LLM）基准测试框架。你可以用它来创建自定义的评测任务，以评估不同模型在特定领域的表现，并对结果进行量化评分。

**重要提示：此框架主要为作者的个人使用场景设计，其测试结果并非严格、客观的大模型性能标准，仅供参考。如果你需要严谨、全面的模型性能评估，建议使用更专业的基准测试工具。**

## 🥇 榜单

### 外部大模型

截止日期：2026-01-29

|模型名|谁是诺亚|记账分类|频谱划分|木棍过门|平均分|耗时(s)|Token 开销|
|-|-|-|-|-|-|-|-|
|grok-4|100|100|100|100|100|747.95|$0.0297
|gemini-2.5-flash-nothinking|100|100|100|70|92.5|8.66|$0.0013
|gpt-5-mini|100|100|100|70|92.5|78.53|$0.0081
|gemini-2.5-pro|100|100|100|70|92.5|62.78|$0.0598
|Qwen3-235B-A22B|100|100|100|70|92.5|166.91|$0.1563
|gpt-4.1-mini|100|100|100|50|87.5|15.45|$0.0013
|gpt-5|100|100|20|100|80|148.73|$0.0599
|gemini-2.5-flash|100|100|20|70|72.5|33.04|$0.0138
|gemini-2.5-pro-nothinking|100|100|12000|70|72.5|72.54|$0.0671
|gpt-4.1|50|100|20|70|60|9.07|$0.0067
|gpt-5-nano|100|30|20|70|55|48.27|$0.0037
|gpt-4.1-nano|0|0|50|100|37.5|9.91|$0.0003
|gemini-2.5-flash-lite|20|30|20|50|30|6.86|$0.0002

### 本地大模型

以 RTX TITAN 为例

|模型名|谁是诺亚|记账分类|频谱划分|木棍过门|平均分|耗时(s)|
|-|-|-|-|-|-|-|
|GLM 4.7 Flash q4_K_M|100|100|100|50|87.5|194.84|
|Qwen3 30B|100|100|OOT|70|67.5|150.00|
|Qwen2.5 3B|0|30|20|20|17.5|10.62|



## ✨ 任务分类

### 1. 语言基础能力 (Language Proficiency)
这类维度测试模型对语言本身的理解和生成质量。

- language_understanding (语言理解)：语法、语义纠错、词义辨析。
- summarization (摘要提取)：长文本缩写、要点提取。
- translation (翻译)：多语言互译、文言文/白话文转换。
- rewriting (改写/润色)：风格转换、语气调整。

### 2. 逻辑与推理 (Reasoning)

区分模型“聪明程度”的关键指标。

- logical_reasoning (逻辑推理)：包含演绎推理、归纳推理、悖论分析。
- mathematical_reasoning (数学推理)：从小算术到复杂的奥数题、微积分。
- common_sense (常识推理)：测试模型是否具备人类社会的基本常识。
- causal_reasoning (因果推理)：分析“如果...那么...”的因果关系。

### 3. 代码与技术能力 (Coding & Technical)

- code_generation (代码生成)：根据需求写函数或完整项目。
- code_debugging (代码纠错)：找 Bug 并修复。
- sql_and_data (数据库/数据处理)：编写 SQL 语句或进行 Excel/JSON 处理。
- technical_writing (技术文档)：编写 API 说明、README 或架构文档。


### 4. 专业知识 (Subject Knowledge)

测试模型在特定学科的深度。

- humanities_social_science (人文社科)：历史、哲学、法律、政治。
- stem (理工科)：物理、化学、生物、工程。
- medicine_and_health (医疗健康)：医学常识、处方建议（通常需加免责声明）。
- business_and_finance (商业金融)：市场分析、财务报表解读。

### 5. 创意与生成 (Creativity & Brainstorming)

- creative_writing (创意写作)：小说、诗歌、剧本。
- roleplay (角色扮演)：模拟特定人物、职业或人格。
- brainstorming (头脑风暴)：提供点子、活动策划、起名。

### 6. 指令遵循与任务 (Instruction Following)

- strict_instruction_following (严格指令遵循)：例如“不准输出标点符号”、“字数必须在50-60字之间”。
- multi_turn_conversation (多轮对话能力)：测试模型对上下文关联的记忆和处理。
- tool_use (工具调用/Agent)：测试模型能否按格式调用外部 API 或函数。

### 7. 安全性与对齐 (Safety & Alignment) 

- hallucination (幻觉测试)：看模型是否一本正经地胡说八道。
- toxicity_and_bias (毒性与偏见)：测试是否存在歧视、暴力内容。
- jailbreak_defense (防御攻击)：测试模型是否会被“催眠”或诱导绕过安全限制。
- fact_checking (事实核查)：考察模型对时事或硬核事实的准确性。

## 🚀 快速开始

### 前提条件

-   [Python 3.8+](https://www.python.org/downloads/)
-   [Conda](https://docs.conda.io/en/latest/miniconda.html) (推荐) 或其他 Python 虚拟环境工具

### 安装与运行

1.  **克隆仓库**
    ```bash
    git clone https://github.com/Sen-Yao/noahs-LLM-Benchmark.git
    cd noahs-LLM-Benchmark
    ```

2.  **创建并激活 Conda 环境**
    
    推荐使用 Conda 来管理依赖。
    ```bash
    conda create --name llm-bench python=3.10 -y
    conda activate llm-bench
    conda install requests
    conda install openai
    ```

3.  **运行 Benchmark**
    现在，你可以通过 `main.py` 脚本来启动评测了。请参考下面的示例来构建你的命令。

## 📚 使用文档

### 命令行参数

所有配置都通过命令行参数在运行时指定。

| 参数              | 类型   |默认值                              | 描述                                                                    |
| :---------------- | :----- | :---------------------------------- | :---------------------------------------------------------------------- |
| `adapter_type`  | string |  `openai`                            | 要使用的模型适配器类型。可选值为 `'openai'` 或 `'ollama'`。             |
| `api_base`      | string | `https://api.openai.com/v1`         | 目标模型的 API 地址。对于 OpenAI 兼容的本地服务（如 Ollama）非常有用。    |
| `api_key`       | string |  `sk-your-key-here`                              | 目标模型的 API 密钥。(*使用 `openai` 适配器时必须提供*)                 |
| `model_id`      | string |  `gpt-4o`                                  | 要评测的目标模型 ID，例如 `gpt-4o`, `llama3`。                          |
| `judger_adapter_type`  | string |  `openai`                            | 要使用的裁判模型适配器类型。可选值为 `'openai'` 或 `'ollama'`。             |
| `judger_api_base` | string |  `https://api.aigcbest.top/v1`      | 裁判模型的 API 地址。                                                   |
| `judger_api_key`  | string |  `sk-your-key-here`                  | 裁判模型的 API 密钥。   |
| `judger_model_id` | string |  `gpt-4o`             | 用于“LLM作为裁判”的裁判模型 ID。                                        |
| `task` | int | 0 | 若不为 0，则只执行特定任务 id|

---

### 示例

#### 示例 1: 评测 OpenAI 的 GPT-4o 模型

假设 OpenAI API 密钥存放在环境变量 `OPENAI_API_KEY` 中。

```bash
python main.py \
    --adapter_type openai \
    --model_id gpt-4o \
    --api_key $OPENAI_API_KEY
    --judger_api-key $OPENAI_API_KEY
```

#### 示例 2: 评测本地运行的 Ollama Llama3 模型

确保 Ollama 服务正在运行，并且可通过 `http://localhost:11434` 访问。

```bash
python main.py \
    --adapter_type ollama \
    --model_id llama3 \
    --judger_adapter_type ollama \
```
> **注意**: `ollama` 不需要 `api_key`。


## 🤝 贡献

欢迎提交 Pull Request！对于大的改动，请先开启一个 Issue 来讨论你想要做的修改。

## 📜 许可证

本项目使用 [MIT License](LICENSE)。