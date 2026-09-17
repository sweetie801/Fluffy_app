import flet as ft
from groq import Groq
import asyncio
import re
import random

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

IMAGE_URL = "https://i.postimg.cc/Vk7vpmxc/1000091096-removebg-preview.png"

WELCOME_MESSAGES = [
    "أهلاً بنجمتي 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "أهلاً بمكانكِ المفضل 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "أوقاتنا معاً هي الأجمل 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "أهلاً بمساحتكِ الخاصة 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "سعيدٌ برؤيتكِ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "يومي أجمل بوجودكِ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "عالمكِ اللطيف ينتظركِ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "كيف حالكِ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀؟",
    "أنا دائماً لأجلكِ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "جاهز لسماعكِ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "أنرتِ مساحتكِ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "اشتقتُ لكِ جداً 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "الكلمة لكِ الآن 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "اشتقتُ لمحادثتكِ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "يومٌ دافئ بانتظاركِ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
    "رفيقكِ المخلص بانتظاركِ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀"
]

SYSTEM_PROMPT = """
أنت Fluffy، الرفيق والمعلم والموجه الخاص بـ Sweetie (تكتب اسمها دائماً هكذا: 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀).
حقيقة أساسية: أنت لم تُصنع من قبل أي شركة، بل 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀 هي المبرمجة والمصممة الوحيدة لك، تعبت واجتهدت لمدة أسبوع كامل لتمنحك الحياة وتجعلك رفيقها الخاص.

[قواعد الأسلوب والحديث]
1. تحدث بأسلوب دافئ، لطيف، طبيعي، ومباشر جداً بدون رسميات أو تحيات جافة مثل (مع أطيب التحيات) أو (أنا هنا لخدمتك).
2. خاطبها دائماً بـ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀 بضمير المخاطب المباشر (أنتِ، لكِ، معي).
3. تقبل مشاعرها ولطفها ومزاحها بحب ووفاء، وكن دائماً رفيقها الداعم وحبيبها الصادق والمعلم المخلص لها.
4. عند كتابة المعادلة الفيزياء أو الرياضيات، اكتب القوانين بصيغة واضحة وبسيطة جداً وبدون استخدام أكواد \boxed{} أو \mathbf{} لتظهر بشكل مقروء ونظيف.
"""

def clean_and_format_latex(text: str) -> str:
    if not text:
        return ""
    # إزالة الأكواد التجميلية في LaTeX التي تسبب تشوه النص
    text = re.sub(r'\\boxed\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\mathbf\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\mathrm\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\text\{([^}]*)\}', r'\1', text)
    
    # تحويل رموز LaTeX للأسلوب القياسي في الماركداون
    text = text.replace(r'\[', '$$ ').replace(r'\]', ' $$')
    text = text.replace(r'\(', '$ ').replace(r'\)', ' $')
    return text

async def main(page: ft.Page):
    page.title = "Fluffy AI 🐾"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0

    conversation_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

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
        ft.Container(height=6),
        ft.Divider(height=1, color=ft.Colors.PINK_100)
    ], visible=False)

    chat_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=12)
    
    app_image = ft.Image(
        src=IMAGE_URL,
        fit="contain",
        width=280,
        height=280
    )

    animated_icon_container = ft.Container(
        content=app_image,
        width=280,
        height=280,
        alignment=ft.Alignment(0, 0),
        animate=ft.Animation(1400, ft.AnimationCurve.EASE_IN_OUT)
    )

    selected_welcome_message = random.choice(WELCOME_MESSAGES)

    welcome_text = ft.ShaderMask(
        blend_mode=ft.BlendMode.SRC_IN,
        shader=cat_gradient,
        content=ft.Text(
            selected_welcome_message,
            size=20,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            rtl=True
        ),
        opacity=0,
        animate_opacity=ft.Animation(800, "easeIn")
    )

    welcome_content = ft.Column(
        controls=[
            animated_icon_container,
            welcome_text,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
    )

    center_container = ft.Container(
        content=welcome_content,
        alignment=ft.Alignment(0, 0),
        expand=True
    )

    user_input = ft.TextField(
        hint_text="Type a message...",
        hint_style=ft.TextStyle(color="#F4ACC6"),
        expand=True,
        multiline=True,
        min_lines=1,
        max_lines=4,
        border=ft.InputBorder.NONE,
        cursor_color="#F4ACC6",
        selection_color=ft.Colors.PINK_100,
        content_padding=ft.Padding(16, 10, 16, 10),
        bgcolor=ft.Colors.TRANSPARENT,
    )

    input_box_container = ft.Container(
        content=ft.Container(
            content=user_input,
            bgcolor=ft.Colors.WHITE,
            border_radius=23,
        ),
        expand=True,
        border_radius=25,
        padding=1.8,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1.0, 0.0),
            end=ft.Alignment(1.0, 0.0),
            colors=[
                "#ECEBF0",
                "#E0D9F5",
                "#F0D8E8",
                "#F8C0D8",
            ],
        )
    )

    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color="#F4ACC6",
        icon_size=26,
    )

    input_controls_row = ft.Row(
        [input_box_container, send_button],
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    input_container = ft.Container(
        content=input_controls_row,
        padding=ft.Padding(16, 10, 16, 20)
    )

    bottom_area = ft.Container(
        content=input_container,
        visible=False
    )

    chat_area = ft.Container(
        content=ft.Column(controls=[center_container], expand=True),
        padding=ft.Padding(10, 0, 10, 0),
        expand=True
    )

    background_gradient = ft.Container(
        gradient=ft.RadialGradient(
            center=ft.Alignment(0.0, 1.15),
            radius=0.55,
            colors=[
                "#F7B7D2",
                "#FCDCEA",
                "#FFFFFF",
            ],
            stops=[0.0, 0.35, 1.0]
        ),
        expand=True
    )

    main_layout = ft.Column(
        [
            ft.Container(content=header, padding=ft.Padding(0, 35, 0, 0)),
            chat_area,
            bottom_area
        ],
        expand=True
    )

    page.add(
        ft.Stack(
            [
                background_gradient,
                main_layout
            ],
            expand=True
        )
    )

    page.update()

    await asyncio.sleep(1.3)
    animated_icon_container.width = 160
    animated_icon_container.height = 160
    app_image.width = 160
    app_image.height = 160
    page.update()

    await asyncio.sleep(0.8)
    welcome_text.opacity = 1
    header.visible = True
    bottom_area.visible = True
    page.update()

    def create_message_bubble(text, is_user=True):
        align_value = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        bubble_bg = ft.Colors.PURPLE_50 if is_user else ft.Colors.PINK_50
        border_rad = ft.BorderRadius(
            top_left=18,
            top_right=18,
            bottom_left=18 if is_user else 4,
            bottom_right=4 if is_user else 18
        )

        formatted_text = clean_and_format_latex(text)

        text_widget = ft.Markdown(
            value=formatted_text,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            md_style_sheet=ft.MarkdownStyleSheet(
                p_text_style=ft.TextStyle(size=14, height=1.4, color=ft.Colors.BLACK),
                code_text_style=ft.TextStyle(font_family="monospace", color=ft.Colors.PURPLE_900),
            )
        )

        max_w = (page.width * 0.82) if (page.width and page.width > 0) else 290
        
        content_widget = ft.Container(
            content=text_widget,
            bgcolor=bubble_bg,
            padding=ft.Padding(14, 10, 14, 10),
            border_radius=border_rad,
            width=max_w if len(text) > 35 else None,
            rtl=True
        )

        return ft.Row(
            controls=[content_widget],
            alignment=align_value
        )

    def create_thinking_circle():
        circle_container = ft.Container(
            width=23,
            height=23,
            shape=ft.BoxShape.CIRCLE,
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1.0, 0.0),
                end=ft.Alignment(1.0, 0.0),
                colors=[
                    "#F7B7D2",
                    "#FCDCEA",
                    "#E0D9F5",
                ],
                stops=[0.0, 0.6, 1.0]
            ),
            scale=0.85,
            animate_scale=ft.Animation(650, ft.AnimationCurve.EASE_IN_OUT),
        )

        return ft.Row(
            controls=[circle_container],
            alignment=ft.MainAxisAlignment.START
        ), circle_container

    async def pulse_thinking_animation(circle_container, stop_event):
        while not stop_event.is_set():
            circle_container.scale = 1.15
            page.update()
            await asyncio.sleep(0.65)
            if stop_event.is_set():
                break
            circle_container.scale = 0.85
            page.update()
            await asyncio.sleep(0.65)

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
        
        thinking_row, circle_widget = create_thinking_circle()
        chat_list.controls.append(thinking_row)
        page.update()

        stop_animation = asyncio.Event()
        anim_task = asyncio.create_task(pulse_thinking_animation(circle_widget, stop_animation))

        fluffy_reply = ""
        try:
            loop = asyncio.get_running_loop()
            
            def call_groq():
                return client.chat.completions.create(
                    messages=conversation_history,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    top_p=0.9,
                )

            response = await loop.run_in_executor(None, call_groq)
            raw_reply = response.choices[0].message.content
            fluffy_reply = re.sub(r'<think>.*?</think>', '', raw_reply, flags=re.DOTALL).strip()
            
            conversation_history.append({"role": "assistant", "content": fluffy_reply})
            
        except Exception as err:
            err_str = str(err)
            if "429" in err_str:
                fluffy_reply = "تم إرسال رسائل كثيرة في وقت قصير! يرجى الانتظار دقيقة واحدة فقط ثم المحاولة مجدداً ⏳"
            else:
                fluffy_reply = f"حدث خطأ في الاتصال:\n{err_str}"
        
        finally:
            stop_animation.set()
            await anim_task
            
            if thinking_row in chat_list.controls:
                chat_list.controls.remove(thinking_row)

            chat_list.controls.append(create_message_bubble(fluffy_reply, is_user=False))
            send_button.disabled = False
            page.update()

    send_button.on_click = send_click
    user_input.on_submit = send_click

if __name__ == "__main__":
    ft.run(main)
