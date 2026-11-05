
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==========================================
# 1. KHOI TAO GEMINI CLIENT
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "Khong tim thay GEMINI_API_KEY trong file .env!"
    )

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"

MAX_HISTORY = 6
MAX_RETRIES = 3

history = []


# ==========================================
# 2. HAM STREAMING CHATBOT
# ==========================================

def streaming_chatbot():

    global history

    print("=" * 50)
    print("       GEMINI STREAMING CHATBOT")
    print("=" * 50)

    print("Model:", MODEL)
    print("Lich su: toi da 3 luot hoi thoai")
    print("Nhap 'exit' de thoat.\n")

    while True:

        prompt = input("Ban: ").strip()

        if prompt.lower() in ["exit", "quit"]:
            print("\nDa thoat chatbot!")
            break

        if not prompt:
            continue

        # Them cau hoi vao lich su
        history.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)]
            )
        )

        history = history[-MAX_HISTORY:]

        answer = ""
        success = False

        print("Gemini: ", end="", flush=True)

        # ==================================
        # 3. STREAMING + RETRY
        # ==================================

        for attempt in range(MAX_RETRIES):

            # Moi lan thu lai bat dau voi noi dung moi
            answer = ""

            try:

                response_stream = client.models.generate_content_stream(
                    model=MODEL,
                    contents=history
                )

                # Nhan tung chunk tu Gemini
                for chunk in response_stream:

                    if chunk.text:
                        print(
                            chunk.text,
                            end="",
                            flush=True
                        )

                        answer += chunk.text

                success = True
                break

            except Exception as e:

                error_message = str(e)

                # Xoa phan tra loi chua hoan chinh
                answer = ""

                if (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                ):

                    if attempt < MAX_RETRIES - 1:

                        wait_time = 2 ** (attempt + 1)

                        print(
                            f"\nGemini dang ban. "
                            f"Thu lai sau {wait_time} giay..."
                        )

                        time.sleep(wait_time)

                    else:

                        print(
                            "\nGemini van dang qua tai "
                            "sau 3 lan thu."
                        )

                else:

                    print("\nLoi API:", e)
                    break

        print()

        # ==================================
        # 4. LUU HISTORY
        # ==================================

        if success and answer:

            history.append(
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=answer)]
                )
            )

            history = history[-MAX_HISTORY:]

        else:

            # Neu that bai, xoa cau hoi vua them
            if history and history[-1].role == "user":
                history.pop()

            print(
                "Khong nhan duoc cau tra loi hoan chinh.\n"
            )


# ==========================================
# 5. CHAY CHUONG TRINH
# ==========================================

if __name__ == "__main__":

    try:
        streaming_chatbot()

    except KeyboardInterrupt:
        print("\n\nChatbot da dung!")
