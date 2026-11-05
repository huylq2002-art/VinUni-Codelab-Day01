
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors


# ==========================================
# 1. LOAD API KEY
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "Khong tim thay GEMINI_API_KEY trong file .env!"
    )


# ==========================================
# 2. INITIALIZE GEMINI CLIENT
# ==========================================

client = genai.Client(api_key=api_key)


# ==========================================
# 3. FUNCTION: CALL GEMINI
# ==========================================

def call_gemini(
    prompt,
    model="gemini-3.5-flash",
    temperature=0.7,
    top_p=1.0,
    max_tokens=1000
):

    # Bat dau do thoi gian
    start = time.time()

    # Cau hinh tham so
    config = types.GenerateContentConfig(
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=max_tokens
    )

    # Goi Gemini API, thu lai neu gap loi 503
    response = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config
            )
            break

        except errors.ServerError:
            if attempt == 2:
                raise

            wait_time = 2 ** (attempt + 1)

            print(
                f"Gemini dang ban. "
                f"Thu lai sau {wait_time} giay..."
            )

            time.sleep(wait_time)

    # Tinh thoi gian phan hoi
    latency = time.time() - start

    # Lay cau tra loi
    answer = response.text or ""

    # Lay thong tin token
    usage = response.usage_metadata

    input_tokens = (
        usage.prompt_token_count if usage else 0
    )

    output_tokens = (
        usage.candidates_token_count if usage else 0
    )

    total_tokens = (
        usage.total_token_count if usage else 0
    )

    # In ket qua
    print("\n========== KET QUA GEMINI ==========")
    print(answer)

    print("\n========== THONG KE ==========")
    print(f"Latency: {latency:.2f} giay")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Total tokens: {total_tokens}")

    # Tra ve dictionary
    return {
        "answer": answer,
        "latency": latency,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens
    }


# ==========================================
# 4. TEST FUNCTION
# ==========================================

if __name__ == "__main__":

    prompt = "AI Engineer la gi? Hay giai thich bang tieng Viet."

    result = call_gemini(
        prompt=prompt,
        model="gemini-3.5-flash",
        temperature=0.7,
        top_p=1.0,
        max_tokens=1000
    )
