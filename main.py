
import os
import time
from dotenv import load_dotenv
from openai import OpenAI

# 1. Doc API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Khong tim thay API Key!")

# 2. Khoi tao OpenAI Client
client = OpenAI(api_key=api_key)


# 3. Xay dung ham call_openai
def call_openai(
    prompt,
    model="gpt-4o-mini",
    temperature=0.7,
    top_p=1.0,
    max_tokens=500
):
    # Bat dau do thoi gian
    start = time.time()

    # Goi OpenAI API
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )

    # Tinh Latency
    latency = time.time() - start

    # Lay cau tra loi
    answer = response.choices[0].message.content

    # Lay thong tin Token
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    # Hien thi ket qua
    print("\n========== KET QUA ==========")
    print("Cau tra loi:")
    print(answer)

    print("\n========== THONG KE ==========")
    print(f"Latency: {latency:.2f} giay")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Total tokens: {input_tokens + output_tokens}")

    return {
        "answer": answer,
        "latency": latency,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }


# 4. Chay thu chuong trinh
if __name__ == "__main__":
    prompt = "AI Engineer la gi? Can hoc nhung kien thuc nao?"

    result = call_openai(prompt)
