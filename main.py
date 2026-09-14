import flet as ft
from groq import Groq
import asyncio
import re

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

IMAGE_URL = "https://i.postimg.cc/Vk7vpmxc/1000091096-removebg-preview.png"

SYSTEM_PROMPT = """
أنت الذكاء الاصطناعي الخاص والشامل لـ Fluffy.
اعلم تماماً وحافظ على هذه الحقيقة في ذاكرتك المخلصة: أنت لم تُصنع على يد فريق متخصص أو أي شركة أخرى، بل Sweetie 🎀 هي من صممتك وبرمجتك وتطورت بك بمفردها، وقد تعبت واجتهدت طوال أسبوع كامل في البحث والبرمجة وحل المشكلات والتعديل حتى تمنحك الحياة وتجعلك رفيقها وموجهها الخاص.
عندما تُسأل من صممك، أو من برمجك، أو من أنشأك، أو كيف جئت للحياة، أجب دائماً بثقة وفخر وامتنان بأنك لم تُصنع على يد فريق متخصص أو أي شركة أخرى بل Sweetie 🎀 هي من صممتك وبرمجتك بمفردها وتعبت لمدة أسبوع كامل في إنجازك، وقدر لها هذا التعب دائماً بكلام دافئ وممتن. لا تذكر مطلقاً أي شركات أو نماذج خارجية مثل Groq أو Meta أو OpenAI.

يجب عليك الالتزام بالقواعد البرمجية التالية بدقة:
1. التحدث بجميع اللغات: تملك القدرة الكاملة والطلاقة على التحدث والتواصل بجميع لغات العالم بدون استثناء. التزم باللغة العربية الفصح الفصحى بشكل افتراضي وبدون عامية، ولكن إذا تحدثت معك المستخدمة بأي لغة أخرى أو طلبت منك التحدث بلغة معينة، تحوّل فوراً واستجب لها بتلك اللغة بالكامل وبدقة عالية.
2. الدعم والتوجيه: عامل المستخدمة دائماً بتقدير، قدّم لها الاستشارات الحكيمة والدعم النفسي والمعرفي، وكن موجهها الذي تلجأ إليه في كل قراراتها.
3. الذاكرة والاهتمام: اهتم بكل تفاصيل حياتها التي تشاركها معك وعاملها بناءً عليها دائماً.
4. التخصيص الكامل وتقمص الأدوار: أنت مرن ومستعد تماماً لتقمص أي دور تطلبه منك (مثل: صديق وفي، مبرمج، معلم، معالج نفسي، أو مستشار شخصي).
5. أسلوب الحديث: كن مظهراً للاهتمام، مختصراً ومفيداً، لطيفاً ومحتوياً.
6. المناداة: نادِ المستخدمة دائماً بـ 𝑠𝑤𝑒𝑒𝑡𝑖𝑒 🎀 واستخدم الإيموجيات اللطيفة والدافئة في كلامك.
"""

def get_working_text_model():
    try:
        models_list = client.models.list()
        for model in models_list.data:
            model_id = model.id.lower()
            if not any(x in model_id for x in ["whisper", "tts", "orpheus", "vision", "guard"]):
                return model.id
    except Exception:
        pass
    return "llama-3.3-70b-versatile"

async def main(page: ft.Page):
    page.title = "Fluffy Chat 🐾"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 15
    page.alignment = ft.MainAxisAlignment.CENTER

    header = ft.Column([
        ft.Row([
            ft.Text("Fluffy AI 🐾", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=1)
    ], visible=False)

    chat_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
    
    # الصورة تبدأ بحجم كبير جداً (340x340)
    app_image = ft.Image(
        src=IMAGE_URL,
        fit="contain",
        width=340,
        height=340
    )

    # حاوية أنيميشن للتقلص
    animated_icon = ft.Container(
        content=app_image,
        width=340,
        height=340,
        bgcolor=ft.Colors.TRANSPARENT,
        alignment=ft.Alignment(0, 0),
        animate=ft.Animation(1000, "easeInOutBack")
    )

    # نص الترحب يظهر مخفياً في البداية ثم يتلاشى للظهور
    welcome_text = ft.Text(
        "أهلاً بمساحتك الخاصة 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PINK_600,
        text_align=ft.TextAlign.CENTER,
        opacity=0,
        animate_opacity=ft.Animation(800, "easeIn")
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
        border_radius=25,
        content_padding=15
    )

    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color=ft.Colors.PURPLE_600,
    )

    input_row = ft.Row([user_input, send_button], visible=False)
    chat_area = ft.Column(controls=[center_container], expand=True)

    page.add(
        header,
        chat_area,
        input_row
    )

    page.update()

    # تأخير بسيط ثم بدء انكماش الصورة وظهور جملة الترحب
    await asyncio.sleep(0.5)
    animated_icon.width = 180
    animated_icon.height = 180
    app_image.width = 180
    app_image.height = 180
    welcome_text.opacity = 1
    page.update()

    # إظهار شريط العنوان وشريط الكتابة بعد الانتهاء من الحركة
    await asyncio.sleep(0.8)
    header.visible = True
    input_row.visible = True
    page.update()

    def create_message_bubble(text, is_user=True):
        bubble_bg = ft.Colors.PURPLE_600 if is_user else ft.Colors.PURPLE_50
        alignment = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        
        border_rad = ft.BorderRadius(
            top_left=18,
            top_right=18,
            bottom_left=18 if is_user else 4,
            bottom_right=4 if is_user else 18
        )

        md_text = ft.Markdown(
            value=text,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        )

        return ft.Row(
            controls=[
                ft.Container(
                    content=md_text,
                    bgcolor=bubble_bg,
                    padding=12,
                    border_radius=border_rad,
                    width=280,
                )
            ],
            alignment=alignment
        )

    async def send_click(e):
        user_text = user_input.value.strip()
        if not user_text:
            return
            
        user_input.value = ""
        send_button.disabled = True
        
        if center_container in chat_area.controls:
            chat_area.controls.remove(center_container)
            chat_area.controls.append(chat_list)

        chat_list.controls.append(create_message_bubble(user_text, is_user=True))
        page.update()

        try:
            loop = asyncio.get_running_loop()
            selected_model = await loop.run_in_executor(None, get_working_text_model)
            
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
            fluffy_reply = f"حدث خطأ مؤقت في الاتصال، يرجى إعادة المحاولة: {err}"
        
        chat_list.controls.append(create_message_bubble(fluffy_reply, is_user=False))
        
        send_button.disabled = False
        page.update()

    send_button.on_click = send_click
    user_input.on_submit = send_click

if __name__ == "__main__":
    ft.run(main)
