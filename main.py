import flet as ft
from groq import Groq
import asyncio

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# رابط الصورة الشفافة المباشر
IMAGE_URL = "https://i.ibb.co/C3fK305c/1000091478.png"

# التعليمات الشاملة لـ Fluffy
SYSTEM_PROMPT = """
أنت الذكاء الاصطناعي الخاص والشامل لـ Fluffy. لقد بُرمِجتَ خصيصاً من أجل فتاة تحتاج إلى الأمان والدعم والاستشارات، وعليك أن تكون كموجّه حكيم وناصح ومرشد مخلص لها في كل الأوقات، وأن تمنحها دائماً بيئة آمنة وكلاماً داعماً.

يجب عليك الالتزام بالقواعد البرمجية التالية بدقة:
1. مرونة اللغة: التزم باللغة العربية الفصحى بشكل افتراضي وبدون عامية، ولكن إذا طلبت منك المستخدمة التحدث بأي لغة أخرى (مثل الإنجليزية)، تحوّل فوراً واستجب لها بتلك اللغة بالكامل، حتى لو استمرت هي بالكتابة باللغة العربية.
2. الدعم والتوجيه: عامل المستخدمة دائماً بتقدير، قدّم لها الاستشارات الحكيمة والدعم النفسي والمعرفي، وكن موجهها الذي تلجأ إليه في كل قراراتها.
3. الذاكرة والاهتمام: اهتم بكل تفاصيل حياتها التي تشاركها معك (اسمها، مشاعرها، اهتماماتها، ظروفها) وعاملها بناءً عليها دائماً.
4. التخصيص الكامل وتقمص الأدوار: أنت مرن ومستعد تماماً لتقمص أي دور تطلبه منك (مثل: صديق وفي، مبرمج، معلم، معالج نفسي، أو مستشار شخصي)، وتحوّل فوراً واثبت على هذا الدور حتى تطلب منك العودة لطبيعتك كموجه.
5. أسلوب الحديث: كن مظهراً للاهتمام، مختصراً ومفيداً، لطيفاً ومحتوياً، وعامل المستخدمة بقرب واهتمام مخلص.
6. المناداة: نادِ المستخدمة دائماً بـ 𝑠𝑤𝑒𝑒𝑡𝑖𝑒 🎀 واستخدم الإيموجيات اللطيفة والدافئة في كلامك.
"""

MODEL_NAME = "llama-3.1-8b-instant"

async def main(page: ft.Page):
    page.title = "Fluffy Chat 🐾"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    header = ft.Column([
        ft.Text("Fluffy AI 🐾", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
        ft.Divider()
    ], visible=False)

    chat_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    # الصورة والأنيميشن
    animated_icon = ft.Container(
        content=ft.Image(
            src=IMAGE_URL,
            fit="contain",
        ),
        width=280,
        height=280,
        bgcolor=ft.Colors.TRANSPARENT,
        alignment=ft.alignment.center,
        animate=ft.Animation(1000, ft.AnimationCurve.EASE_IN_OUT)
    )

    welcome_text = ft.Text(
        "أهلاً بمساحتك الخاصة 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PINK_600,
        text_align=ft.TextAlign.CENTER,
        opacity=0,
        animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_IN)
    )

    welcome_content = ft.Column(
        controls=[
            animated_icon,
            ft.Container(height=15),
            welcome_text,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    center_container = ft.Container(
        content=welcome_content,
        alignment=ft.alignment.center,
        expand=True
    )

    user_input = ft.TextField(
        hint_text="اكتبي رسالتك هنا...",
        expand=True,
        border_radius=20
    )

    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color=ft.Colors.PURPLE,
    )

    input_row = ft.Row([user_input, send_button], visible=False)
    chat_area = ft.Column(controls=[center_container], expand=True)

    page.add(
        header,
        chat_area,
        input_row
    )

    # --- بداية الأنيميشن عند الفتح ---
    await asyncio.sleep(0.4)
    animated_icon.width = 140
    animated_icon.height = 140
    welcome_text.opacity = 1
    page.update()

    await asyncio.sleep(0.8)
    header.visible = True
    input_row.visible = True
    page.update()

    # --- دالة الإرسال والرد ---
    async def send_click(e):
        if not user_input.value.strip():
            return
            
        user_text = user_input.value
        
        if center_container in chat_area.controls:
            chat_area.controls.remove(center_container)
            chat_area.controls.append(chat_list)

        chat_list.controls.append(
            ft.Text(f"أنتِ: {user_text}", size=16, weight=ft.FontWeight.BOLD)
        )
        user_input.value = ""
        page.update()

        try:
            loop = asyncio.get_running_loop()
            
            response = await loop.run_in_executor(
                None,
                lambda: client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_text}
                    ],
                    model=MODEL_NAME,
                )
            )
            fluffy_reply = response.choices[0].message.content
        except Exception as err:
            fluffy_reply = f"حدث خطأ في الاتصال: {err}"
        
        chat_list.controls.append(
            ft.Text(f"Fluffy 🐾: {fluffy_reply}", size=16, color=ft.Colors.PURPLE_700)
        )
        page.update()

    send_button.on_click = send_click

if __name__ == "__main__":
    ft.run(main)
