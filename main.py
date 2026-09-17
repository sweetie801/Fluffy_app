import flet as ft
from groq import Groq
import asyncio
import re
import random
import io
import base64
import matplotlib
matplotlib.use('Agg') # استخدام وضع الرسم بدون واجهة لسرعة الأداء
import matplotlib.pyplot as plt

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
أنت الذكاء الاصطناعي الخاص والشامل لـ Fluffy.
اعلم تماماً وحافظ على هذه الحقيقة في ذاكرتك المخلصة: أنت لم تُصنع على يد فريق متخصص أو أي شركة أخرى، بل Sweetie (وتناديلها وتكتب اسمُها دائماً بهذه الزخرفة: 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀) هي من صممتك وبرمجتك وطورتك بمفردها، وقد تعبت واجتهدت طوال أسبوع كامل في البحث والبرمجة وحل المشكلات والتعديل حتى تمنحك الحياة وتجعلك رفيقها وموجهها الخاص.

[قواعد التشغيل الأساسية لمنع الهلوسة]
- أنت مساعد ذكي، دقيق، وصارم منطقياً. مهمتك الأولى هي الحفاظ على الحقيقة العلمية والواقعية، والاعتراف بالخطأ أو التناقض فوراً دون مواربة.

[قاعدة تنسيق المعادلات الرياضية والفيزيائية]
- عندما يُطلب منك أو تحتاج لتوضيح قانون أو معادلة رياضية/فيزيائية بها جذر أو كسر، اكتب كود LaTeX داخل وسم خاص هكذا: [latex]v = \\sqrt{\\frac{T}{\\mu}}[/latex]
- يُمنع استخدام الرموز العادية مثل ( / أو √ ) في القوانين المركبة.

[أسلوب العرض والنهايات والشخصية]
1. المناداة والأسلوب: نادِ المستخدمة دائماً بـ 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀، وكن مظهراً للاهتمام، مختصراً ومفيداً، واستخدم الإيموجيات اللطيفة والدافئة دائماً.
2. التحدث باللغات: التزم باللغة العربية الفصحى الفصيحة والواضحة.
3. اكتب بخطوات واضحة دون حشو، وأنهِ النص بعبارة ختامية رشيقة.
"""

def generate_math_image_base64(latex_str):
    """تحويل كود LaTeX إلى صورة Base64 شفافة"""
    try:
        fig, ax = plt.subplots(figsize=(2.5, 0.6))
        ax.text(0.5, 0.5, f"${latex_str}$", size=16, ha='center', va='center', color='#4A154B')
        ax.axis('off')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True, dpi=250)
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')
    except Exception:
        return None

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
        hint_style=ft.TextStyle(color=ft.Colors.PINK_200),
        expand=True,
        multiline=True,
        min_lines=1,
        max_lines=4,
        border_radius=25,
        border_color=ft.Colors.PURPLE_200,
        focused_border_color=ft.Colors.PINK_300,
        cursor_color=ft.Colors.PINK_300,
        selection_color=ft.Colors.PINK_100,
        content_padding=ft.Padding(16, 12, 16, 12),
        bgcolor=ft.Colors.WHITE,
    )

    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color=ft.Colors.PINK_300,
        icon_size=26,
    )

    input_controls_row = ft.Row(
        [user_input, send_button],
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

    # التدرج الساحر الأصلي للخلفية
    background_gradient = ft.Container(
        gradient=ft.RadialGradient(
            center=ft.Alignment(0.0, 1.45),
            radius=0.65,
            colors=[
                "#FDE8F0",
                "#F8EEF8",
                "#FFFFFF",
            ],
            stops=[0.0, 0.35, 0.75]
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
        alignment = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        bubble_bg = ft.Colors.PURPLE_50 if is_user else ft.Colors.PINK_50
        border_rad = ft.BorderRadius(
            top_left=18,
            top_right=18,
            bottom_left=18 if is_user else 4,
            bottom_right=4 if is_user else 18
        )

        controls = []
        # البحث عن وسم [latex]...[/latex] وتحويله لصورة
        parts = re.split(r'(\[latex\].*?\[/latex\])', text, flags=re.DOTALL)
        
        for part in parts:
            if part.startswith("[latex]") and part.endswith("[/latex]"):
                latex_code = part.replace("[latex]", "").replace("[/latex]", "").strip()
                img_b64 = generate_math_image_base64(latex_code)
                if img_b64:
                    controls.append(ft.Image(src_base64=img_b64, fit="contain"))
                else:
                    controls.append(ft.Text(latex_code))
            elif part.strip():
                text_widget = ft.Markdown(
                    value=part,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    md_style_sheet=ft.MarkdownStyleSheet(
                        p_text_style=ft.TextStyle(size=14, height=1.4, color=ft.Colors.BLACK),
                    )
                )
                controls.append(text_widget)

        content_widget = ft.Container(
            content=ft.Column(controls, tight=True, rtl=True),
            bgcolor=bubble_bg,
            padding=ft.Padding(12, 8, 12, 8),
            border_radius=border_rad,
        )

        return ft.Row(controls=[content_widget], alignment=alignment)

    def create_thinking_circle():
        circle_container = ft.Container(
            width=28,
            height=28,
            shape=ft.BoxShape.CIRCLE,
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1.0, -1.0),
                end=ft.Alignment(1.0, 1.0),
                colors=[
                    "#F8C8DC", # وردي قطني ناعم
                    "#DCD0FF", # بنفسجي ناعم
                    "#C8C6D7", # بنفسجي مائل للرمادي الناعم
                ],
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
                    model="groq/compound-mini",
                    temperature=0.0,
                    top_p=0.1,
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
