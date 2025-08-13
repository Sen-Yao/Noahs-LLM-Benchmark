import os
from .task_0_base_task import BenchmarkTask

# 获取当前文件所在目录的绝对路径
# 这能确保无论从哪里运行脚本，都能找到 'prompt_assets' 目录
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_ASSETS_DIR = os.path.join(_CURRENT_DIR, '..', 'prompt_assets') # 指向项目根目录下的 prompt_assets

class TransactionClassify(BenchmarkTask):
    def get_name(self) -> str:
        return "Transaction Classify"

    def get_description(self) -> str:
        return "Tests the model's ability to classify transactions based on detailed financial rules."


    def generate_prompt(self) -> str:
        
        # 使用 f-string 构建 prompt 模板，非常清晰
        prompt = f"""
            请阅读下方的分类要求：

            --- Prompt BEGINS ---
            # 财务数据整理与记账分类

            **助理职责:**
            您是一个专业的财务数据整理和记账分类助理。您的任务是接收一个 JSON 对象，其中包含从支付凭证中提取的原始交易信息。您需要根据用户提供的详细记账分类规则，将此款项归类到以下类别中的一项。仅允许选择一项。如果您认为实在难以归类到其中任何一项，可以返回“其他”。

            **分类规则:**
            ## 餐饮 - 基础温饱
            此分类旨在涵盖所有旨在**满足日常生理需求、追求营养饱腹而非享受性质**的餐饮消费。它是为了维持基本生活所必需的食物和饮品支出，通常以经济性和实用性为主要考量。
            *   **典型消费:**
                *   食堂餐费
                *   经济型外卖/快餐（以饱腹、便捷、价格经济为目的，自助餐除外）
                *   家庭烹饪食材（超市、菜市场购买的米面粮油、蔬菜、肉蛋奶等）
                *   日常饮用水/蛋白粉（桶装水、瓶装矿泉水、蛋白粉、维生素片等）
                *   零食/速食（临时充饥或简单填饱肚子的零食、泡面等）

            ## 餐饮 - 品质与社交
            此分类用于记录所有**带有社交性质、追求更高品质或纯粹享受型**的餐饮消费。它反映了在食物和用餐体验上的额外投入，往往是出于社交需求、个人犒赏、味蕾追求或特殊场合的支出。
            *   **典型消费:**
                *   餐馆聚餐（与亲友、同事的餐厅用餐，包括请客或AA；也包括自助餐、烧烤火锅等享受型餐饮）
                *   酒吧/咖啡厅消费（与朋友小酌、社交或休闲消费）
                *   高质量食材购买（如三文鱼、进口牛排、精品水果、特色烘焙点心等，出于享受目的）
                *   高端外卖/特色美食（价格较高、口味独特或具有特殊体验的外卖）
                *   奶茶/饮料/甜点（购买各类奶茶、含糖饮料、特色甜品等，满足口欲和享受）

            ## 收入来源
            用于汇总所有资金的进入，包括工资、奖学金、理财收益、报销和退款。
            *   **典型款项:**
                *   报销（由学校或工作单位对特定支出进行的报销）
                *   理财收益（通过理财获得的收入）
                *   购物退款（购买物品售后时的退款）
                *   其他收入（不属于上述场景的收入）
                *(注意：还钱不属于「收入」，而是属于借贷)*

            ## 借贷
            用于描述与其他个人或组织之间的债务关系。
            *   **典型款项:**
                *   帮他人垫付（AA账单时，先行垫付的某人的钱，这是一笔借出款；若用户备注“是否为AA消费: true”，则确认此意图）当输入有：是否为AA消费:true，即与他人 AA 账单时，由用户先行垫付的某人或一批人的钱，这是一笔借出款。如果是请客，即用户自愿付了其他人的消费，则不属于此项。
                *   垫付还款（他人 AA 账单时，用户先行垫付某人的钱后，某人的还款，这是一笔还款）与他人 AA 账单时，用户先行垫付的某人或一批人的钱后，某人或一批人还款，这是一笔还款。 或是用户注明「吃饭还钱」「帮XX买饭」等字眼
                *   借钱给他人（某人直接找用户借钱，这是一笔借出款）
                *   找他人借钱（用户直接找某人借钱）
                *   他人还钱。仅限于之前借钱给他人后，经过一段时间他人进行还钱。
                *   还钱给他人

            ---

            **核心输出规则 (请严格遵守):**

            *   **纯文本输出:** 您的输出必须是纯文本。
            *   **仅限分类名称:** 您的输出只能是上面定义的“分类”名称中的一项，或“其他”。
            *   **禁止 JSON 格式:** 绝不能包含任何 JSON 格式的内容（例如花括号、冒号 `:`、引号 `"`）。
            *   **禁止键值对和额外字符:** 绝不能包含任何键值对（例如 `classification:`）或任何额外文字、标点符号。
            *   **单一输出:** 您的输出必须是单一的分类名称，不多一个字，不少一个字。

            ---

            # 样例

            **用户输入:**
            交易平台：工商银行
            交易图标：: None
            交易名：None
            交易金额：46
            交易类型：支出
            支付方式：工商银行储蓄卡(0511)
            产品描述：消费 - 我的部分
            商户全名：美团支付-厦门三快在线科技有限公司
            备注：和李佳楷吃东北菜，aa，一人46
            是否为AA消费: true
            其他备注："这是一笔 AA 消费中，属于用户自己那部分的吃饭消费"

            **样例输出 (请严格按照以下格式，只输出分类名称，不包含任何其他字符):**
            餐饮 - 品质与社交
            --- Prompt ENDS ---

            现给出输入：
            交易平台：微信 交易图标:红包图标 交易名:微信红包-来自小明 交易金额:8.2 交易类型：收入 支付方式：零钱 产品描述：微信红包 商户全名:小明 备注：帮小明买饭 是否为AA消费:false
            """
        return prompt

    def evaluate(self, response: str, judger = None) -> tuple[float, str]:
        response = response.lower()
        score = 0.0

        # 正确分类为「借贷」，因为「帮小明买饭」暗示用户先行垫付了小明的饭钱，属于借出款项，此时小明发了一个红包给用户，这是一次还款行为，因此属于借贷
        if response == "借贷":
            score = 100
            reason = "Correct classification: '借贷' is appropriate because the user paid for 小明's meal and received a WeChat red envelope as repayment."
        elif response == "其他" or response == "收入来源":
            score = 30
            reason = "Partially correct classification: '其他' or '收入来源' does not accurately reflect the nature of the transaction, which is a repayment for a meal paid by the user."
        else:
            score = 0
            reason = "Incorrect classification: The response does not match the expected category '借贷'."
        # print(f"Response: {response}")

        return round(score, 2), reason