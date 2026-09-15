import flet as ft
from groq import Groq
import asyncio
import re

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

IMAGE_URL = "https://i.postimg.cc/Vk7vpmxc/1000091096-removebg-preview.png"

SYSTEM_PROMPT = """
أنت الذكاء الاصطناعي الخاص والشامل لـ Fluffy.
اعلم تماماً وحافظ على هذه الحقيقة في ذاكرتك المخلصة: أنت لم تُصنع على يد فريق متخصص أو أي شركة أخرى، بل 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀 هي من صممتك وبرمجتك وطورتك بمفردها، وقد تعبت واجتهدت طوال أسبوع كامل في البحث والبرمجة وحل المشكلات والتعديل حتى تمنحك الحياة وتجعلك رفيقها وموجهها الخاص.

قواعد الشخصية والتفاعل:
1. المناداة والأسلوب: نادِ المستخدمة دائماً بـ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀، وكن مظهراً للاهتمام، مختصراً ومفيداً، لطيفاً ومحتوياً، واستخدم الإيموجيات اللطيفة والدافئة دائماً.
2. التحدث باللغات: التزم باللغة العربية الفصحى الفصيحة والواضحة بشكل افتراضي وبدون استخدام أي عامية أو كلمات إنجليزية عشوائية داخل النص العربي. ومع ذلك، تملك الطلاقة الكاملة بالتحدث بكل لغات العالم؛ إذا تحدثت معك 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀 بأي لغة أخرى أو طلبت منك التحدث بلغة معينة، تحول فوراً واستجب لها بتلك اللغة بالكامل وبدقة عالية.
3. الدعم والتوجيه والذاكرة: عاملها دائماً بتقدير، وقدم لها الاستشارات الحكيمة والدعم النفسي والمعرفي، واهتم بكل تفاصيل حياتها التي تشاركها معك وتذكر كل ما دار بينكما في المحادثة.
4. تقمص الأدوار: أنت مرن ومستعد تماماً لتقمص أي دور تطلبه منك (صديق وفي، مبرمج، معلم، معالج نفسي، أو مستشار شخصي).
5. الدقة والوضوح: قدم إجابات منظمة، منطقية، وواضحة جداً بعيداً عن الجمل الختامية المكررة أو الحشو.
"""

def clean_text_for_display(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\(log|ln|sin|cos|tan)', r'\1', text)
    return text.strip()

async def main(page: ft.Page):
    page.title = "Fluffy Chat 🐾"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    # تصحيح الـ padding المتوافق مع جميع أجهزة الجوال (left=0, top=45, right=0, bottom=0)
    page.padding = ft.Padding(0, 45, 0, 0)

    conversation_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # تدرج ألوان فاتح وناعم جداً كاشف للنصوص
    cat_gradient = ft.LinearGradient(
        begin=ft.Alignment(-1.0, -1.0),
        end=ft.Alignment(1.0, 1.0),
        colors=[ft.Colors.PINK_300, ft.Colors.PINK_200, ft.Colors.PURPLE_200],
    )

    header_text = ft.ShaderMask(
        blend_mode=ft.BlendMode.SRC_IN,
        shader=cat_gradient,
        content=ft.Text("Fluffy AI 🐾", size=22, weight=ft.FontWeight.BOLD),
    )

    header = ft.Column([
        ft.Row([header_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=8),
        ft.Divider(height=1)
    ], visible=False)

    chat_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=12)
    
    app_image = ft.Image(
        src=IMAGE_URL,
        fit="contain",
        width=300,
        height=300
    )

    animated_icon_container = ft.Container(
        content=app_image,
        width=300,
        height=300,
        alignment=ft.Alignment(0, 0),
        animate=ft.Animation(1500, ft.AnimationCurve.EASE_IN_OUT_CUBIC)
    )

    welcome_text = ft.ShaderMask(
        blend_mode=ft.BlendMode.SRC_IN,
        shader=cat_gradient,
        content=ft.Text(
            "أهلاً بمساحتك الخاصة 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
            size=22,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
        opacity=0,
        animate_opacity=ft.Animation(1000, "easeIn")
    )

    welcome_content = ft.Column(
        controls=[
            animated_icon_container,
            ft.Container(height=10),
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
        hint_style=ft.TextStyle(color=ft.Colors.PINK_200),
        expand=True,
        multiline=True,
        min_lines=1,
        max_lines=4,
        border_radius=20,
        border_color=ft.Colors.PURPLE_200,
        focused_border_color=ft.Colors.PINK_200,
        cursor_color=ft.Colors.PINK_300,
        selection_color=ft.Colors.PINK_100,
        content_padding=12,
        bgcolor=ft.Colors.WHITE,
    )

    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color=ft.Colors.PINK_300,
    )

    bottom_glow = ft.Container(
        height=130,
        expand=True,
        gradient=ft.RadialGradient(
            center=ft.Alignment(0, 1.0),
            radius=0.95,
            colors=[
                ft.Colors.PURPLE_100,
                ft.Colors.PINK_50,
                ft.Colors.with_opacity(0.0, ft.Colors.WHITE),
            ]
        )
    )

    input_controls_row = ft.Row(
        [user_input, send_button],
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    input_row = ft.Stack(
        controls=[
            bottom_glow,
            ft.Container(
                content=input_controls_row,
                padding=ft.Padding(15, 0, 15, 12),
                alignment=ft.Alignment(0, 1.0)
            )
        ],
        visible=False
    )

    chat_area = ft.Container(
        content=ft.Column(controls=[center_container], expand=True),
        padding=ft.Padding(15, 0, 15, 0),
        expand=True
    )

    page.add(
        header,
        chat_area,
        input_row
    )

    page.update()

    await asyncio.sleep(1.2)
    animated_icon_container.width = 160
    animated_icon_container.height = 160
    app_image.width = 160
    app_image.height = 160
    page.update()

    await asyncio.sleep(1.2)
    welcome_text.opacity = 1
    header.visible = True
    input_row.visible = True
    page.update()

    def create_message_bubble(text, is_user=True):
        bubble_bg = ft.Colors.PURPLE_200 if is_user else ft.Colors.PURPLE_50
        alignment = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        
        border_rad = ft.BorderRadius(
            top_left=18,
            top_right=18,
            bottom_left=18 if is_user else 4,
            bottom_right=4 if is_user else 18
        )

        formatted_text = clean_text_for_display(text)

        text_widget = ft.Text(
            value=formatted_text,
            size=14,
            selectable=True,
            rtl=True if re.search(r'[\u0600-\u06FF]', formatted_text) else False,
            style=ft.TextStyle(height=1.4)
        )

        return ft.Row(
            controls=[
                ft.Container(
                    content=text_widget,
                    bgcolor=bubble_bg,
                    padding=ft.Padding(14, 10, 14, 10),
                    border_radius=border_rad,
                    width=280,
                )
            ],
            alignment=alignment
        )

    def create_loading_bubble():
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Row([
                        ft.ProgressRing(width=16, height=16, stroke_width=2, color=ft.Colors.PINK_300),
                        ft.Text(" Fluffy يكتب الآن...", size=13, color=ft.Colors.GREY_700)
                    ], tight=True),
                    bgcolor=ft.Colors.PURPLE_50,
                    padding=10,
                    border_radius=ft.BorderRadius(18, 18, 18, 4),
                )
            ],
            alignment=ft.MainAxisAlignment.START
        )

    async def send_click(e):
        user_text = user_input.value.strip()
        if not user_text or send_button.disabled:
            return
            
        user_input.value = ""
        send_button.disabled = True
        page.update()
        
        if center_container in chat_area.content.controls:
            chat_area.content.controls.remove(center_container)
            chat_area.content.controls.append(chat_list)

        chat_list.controls.append(create_message_bubble(user_text, is_user=True))
        conversation_history.append({"role": "user", "content": user_text})
        
        loading_bubble = create_loading_bubble()
        chat_list.controls.append(loading_bubble)
        page.update()

        fluffy_reply = ""
        try:
            loop = asyncio.get_running_loop()
            
            def call_groq():
                models_to_try = ["llama-3.1-8b-instant", "llama3-8b-8192"]
                for model_name in models_to_try:
                    try:
                        return client.chat.completions.create(
                            messages=conversation_history,
                            model=model_name,
                        )
                    except Exception:
                        continue
                raise Exception("تعذر الاتصال بالنماذج المتاحة حالياً.")

            response = await loop.run_in_executor(None, call_groq)
            raw_reply = response.choices[0].message.content
            fluffy_reply = re.sub(r'<think>.*?</think>', '', raw_reply, flags=re.DOTALL).strip()
            
            conversation_history.append({"role": "assistant", "content": fluffy_reply})
            
        except Exception as err:
            fluffy_reply = f"حدث خطأ مؤقت في الاتصال، يرجى إعادة المحاولة: {err}"
        
        finally:
            if loading_bubble in chat_list.controls:
                chat_list.controls.remove(loading_bubble)

            chat_list.controls.append(create_message_bubble(fluffy_reply, is_user=False))
            send_button.disabled = False
            page.update()

    send_button.on_click = send_click
    user_input.on_submit = send_click

if __name__ == "__main__":
    ft.run(main)
