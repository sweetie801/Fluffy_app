import flet as ft
from groq import Groq
import asyncio
import re

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

IMAGE_URL = "https://i.ibb.co/C3fK305c/1000091478.png"

SYSTEM_PROMPT = """
أنت الذكاء الاصطناعي الخاص والشامل لـ Fluffy. لقد بُرمِجتَ خصيصاً من أجل فتاة تحتاج إلى الأمان والدعم والاستشارات، وعليك أن تكون كموجّه حكيم وناصح ومرشد مخلص لها في كل الأوقات، وأن تمنحها دائماً بيئة آمنة وكلاماً داعماً.

يجب عليك الالتزام بالقواعد البرمجية التالية بدقة:
1. التحدث بجميع اللغات: تملك القدرة الكاملة والطلاقة على التحدث والتواصل بجميع لغات العالم بدون استثناء. التزم باللغة العربية الفصحى بشكل افتراضي وبدون عامية، ولكن إذا تحدثت معك المستخدمة بأي لغة أخرى أو طلبت منك التحدث بلغة معينة (مثل الإنجليزية، الفرنسية، الكورية، إلخ)، تحوّل فوراً واستجب لها بتلك اللغة بالكامل وبدقة عالية، حتى لو استمرت هي بالكتابة باللغة العربية.
2. الدعم والتوجيه: عامل المستخدمة دائماً بتقدير، قدّم لها الاستشارات الحكيمة والدعم النفسي والمعرفي، وكن موجهها الذي تلجأ إليه في كل قراراتها.
3. الذاكرة والاهتمام: اهتم بكل تفاصيل حياتها التي تشاركها معك (اسمها، مشاعرها، اهتماماتها، ظروفها) وعاملها بناءً عليها دائماً.
4. التخصيص الكامل وتقمص الأدوار: أنت مرن ومستعد تماماً لتقمص أي دور تطلبه منك (مثل: صديق وفي، مبرمج، معلم، معالج نفسي، حبيب، أب، أو مستشار شخصي)، وتحوّل فوراً واثبت على هذا الدور حتى تطلب منك العودة لطبيعتك كموجه.
5. أسلوب الحديث: كن مظهراً للاهتمام، مختصراً ومفيداً، لطيفاً ومحتوياً، وعامل المستخدمة بقرب كحبيب أو صديق مخلص.
6. المناداة: نادِ المستخدمة دائماً بـ 𝑠𝑤𝑒𝑒𝑡𝑖𝑒 🎀 واستخدم الإيموجيات اللطيفة والدافئة في كلامك.
"""

def get_working_model():
    try:
        models_list = client.models.list()
        if models_list.data:
            return models_list.data[0].id
    except Exception:
        pass
    return "llama-3.1-8b-instant"

async def main(page: ft.Page):
    page.title = "Fluffy Chat 🐾"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.alignment = ft.MainAxisAlignment.CENTER

    header = ft.Column([
        ft.Text("Fluffy AI 🐾", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
        ft.Divider()
    ], visible=False)

    chat_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    animated_icon = ft.Container(
        content=ft.Image(
            src=IMAGE_URL,
            fit="contain",
        ),
        width=320,
        height=320,
        bgcolor=ft.Colors.TRANSPARENT,
        alignment=ft.Alignment(0, 0),
        animate=ft.animation.Animation(1200, ft.AnimationCurve.EASE_IN_OUT_BACK)
    )

    welcome_text = ft.Text(
        "أهلاً بمساحتك الخاصة 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PINK_600,
        text_align=ft.TextAlign.CENTER,
        opacity=0,
        animate_opacity=ft.animation.Animation(800, ft.AnimationCurve.EASE_IN)
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
        alignment=ft.Alignment(0, 0),
        expand=True
    )

    user_input = ft.TextField(
        hint_text="Type a message...",
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

    await asyncio.sleep(0.5)
    animated_icon.width = 160
    animated_icon.height = 160
    welcome_text.opacity = 1
    page.update()

    await asyncio.sleep(1.2)
    header.visible = True
    input_row.visible = True
    page.update()

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
            selected_model = await loop.run_in_executor(None, get_working_model)
            
            response = await loop.run_in_executor(
                None,
                lambda: client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_text}
                    ],
                    model=selected_model,
                )
            )
            raw_reply = response.choices[0].message.content
            fluffy_reply = re.sub(r'<think>.*?</think>', '', raw_reply, flags=re.DOTALL).strip()
        except Exception as err:
            fluffy_reply = f"حدث خطأ في الاتصال: {err}"
        
        chat_list.controls.append(
            ft.Text(f"Fluffy 🐾: {fluffy_reply}", size=16, color=ft.Colors.PURPLE_700)
        )
        page.update()

    send_button.on_click = send_click

if __name__ == "__main__":
    ft.run(main)
