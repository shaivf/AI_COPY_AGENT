# requirements: pip install openai pandas
import openai
import random
import pandas as pd

# 配置你的 OpenAI API Key
openai.api_key = "YOUR_API_KEY"

def generate_copy(theme: str, num_variants: int = 50) -> list:
    """
    根据活动主题生成多版本文案
    :param theme: 活动主题
    :param num_variants: 生成文案数量
    :return: 文案列表
    """
    copies = []
    for i in range(num_variants):
        prompt = f"请为市场活动主题 '{theme}' 创作一条创意营销文案，风格吸引用户点击，语言简洁有力。"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        copy_text = response['choices'][0]['message']['content'].strip()
        copies.append(copy_text)
    return copies

def simulate_ab_test(copies: list) -> pd.DataFrame:
    """
    模拟 A/B 测试效果，并根据模拟结果调整下一轮生成策略
    :param copies: 文案列表
    :return: 带点击率和优化提示的 DataFrame
    """
    results = []
    for copy in copies:
        ctr = round(random.uniform(0.05, 0.3), 2)
        # 简单优化建议
        if ctr < 0.1:
            suggestion = "尝试调整文案标题或强调优惠点"
        elif ctr < 0.2:
            suggestion = "可以增加视觉元素或行动号召"
        else:
            suggestion = "表现良好，可用于下一轮测试"
        results.append({"copy": copy, "click_through_rate": ctr, "suggestion": suggestion})
    
    df = pd.DataFrame(results)
    df = df.sort_values(by="click_through_rate", ascending=False).reset_index(drop=True)
    return df

if __name__ == "__main__":
    theme = input("请输入市场活动主题: ")
    print("\n生成文案中...")
    variants = generate_copy(theme, num_variants=50)
    
    print("\nA/B 测试模拟结果:")
    ab_results = simulate_ab_test(variants)
    print(ab_results.head(10))  # 显示前 10 条最佳文案
    
    # 保存结果
    ab_results.to_csv("ab_test_results.csv", index=False)
    print("\n结果已保存到 ab_test_results.csv")
