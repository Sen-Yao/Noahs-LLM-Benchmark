# Noah's LLM Benchmark

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

个人使用的大语言模型（LLM）基准测试框架。你可以用它来创建自定义的评测任务，以评估不同模型在特定领域的表现，并对结果进行量化评分。

**重要提示：此框架主要为作者的个人使用场景设计，其测试结果并非严格、客观的大模型性能标准，仅供参考。如果你需要严谨、全面的模型性能评估，建议使用更专业的基准测试工具。**

## 🥇 榜单

截止日期：2025-08-13

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

## ✨ 特性

-   **高度模块化**: 评测任务和模型适配器完全分离，添加新的测试单元或接入新的模型服务变得异常简单。
-   **灵活的模型接入**: 内置对 OpenAI GPT 系列和本地 Ollama 服务的适配器，可轻松扩展到任何其他 API。
-   **可量化的评估**: 支持多种评估方式，包括基于关键词的评分、基于代码执行结果的评分，以及结构化输出的验证。
-   **清晰的报告**: 在测试结束后生成详细的报告，包含每个任务的得分、耗时、模型输出和评分理由。

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
| `eval_api_base` | string |  `https://api.aigcbest.top/v1`      | 裁判模型的 API 地址。                                                   |
| `eval_api_key`  | string |  `sk-your-key-here`                  | 裁判模型的 API 密钥。   |
| `eval_model_id` | string |  `gpt-4o`             | 用于“LLM作为裁判”的裁判模型 ID。                                        |
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
    --eval_api-key $OPENAI_API_KEY
```

#### 示例 2: 评测本地运行的 Ollama Llama3 模型

确保 Ollama 服务正在运行，并且可通过 `http://localhost:11434` 访问。

```bash
python main.py \
    --adapter_type ollama \
    --model_id llama3
```
> **注意**: `ollama` 不需要 `api_key`。


## 🤝 贡献

欢迎提交 Pull Request！对于大的改动，请先开启一个 Issue 来讨论你想要做的修改。

## 📜 许可证

本项目使用 [MIT License](LICENSE)。