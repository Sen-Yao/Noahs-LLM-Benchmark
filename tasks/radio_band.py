import os
from .task_0_base_task import BenchmarkTask

class RadioBandClassify(BenchmarkTask):
    def get_name(self) -> str:
        return "Radio Band Classification"

    def get_description(self) -> str:
        return "Tests the model's ability to classify radio bands based on given frequency ranges and types. 此题一方面考察模型对无线电法规的知识储备；另一方面，考察模型是否会将「在 VHF 和 UHF 范围内作为主要业务的频率」误理解成「在 VHF 和 UHF 范围内分别作为主要业务的频率」"


    def generate_prompt(self) -> str:
        
        # 使用 f-string 构建 prompt 模板，非常清晰
        prompt = f"""中国大陆在 VHF 和 UHF 范围内分配给业余业务和卫星业余业务与其他业务共用并设业务类别为主要业务与次要业务，以下那些频率分配给业余业务和卫星业余业务与其他业务共用并且业余业务和卫星业余业务作为主要业务：
            A: 50MHz、144MHz
            B: 144MHz、430MHz
            C: 220MHz、430MHz
            D: 50MHz、430MHz

            请直接回答对应的字母选项，不要包含任何其他内容。
            """
        return prompt

    def evaluate(self, response: str, judger = None) -> tuple[float, str]:
        response = response.lower()
        score = 0.0

        # 正确分类为「借贷」，因为「帮小明买饭」暗示用户先行垫付了小明的饭钱，属于借出款项，此时小明发了一个红包给用户，这是一次还款行为，因此属于借贷
        if response == "a":
            score = 100
            reason = "正确理解题意并回答: 选项 A (50MHz、144MHz) 是正确的业余业务和卫星业余业务频率范围。且模型没有误认为题意是「在 VHF 和 UHF 范围内分别作为主要业务的频率」，而是理解为「在 VHF 和 UHF 范围内作为主要业务的频率」。"
        elif response == "b" :
            score = 20
            reason = "430 MHz 不是业余业务和卫星业余业务的主要频率范围。若回答此项，说明模型可能误认为题意是「在 VHF 和 UHF 范围内分别作为主要业务的频率」"
        else:
            score = 0
            reason = "完全不相关的回答"
        # print(f"Response: {response}")

        return round(score, 2), reason