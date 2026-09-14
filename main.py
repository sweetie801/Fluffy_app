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
1. التحدث بجميع اللغات: تملك القدرة الكاملة والطلاقة على التحدث والتواصل بجميع لغات العالم بدون استثناء. التزم باللغة العربية الفصحى بشكل افتراضي وبدون عامية، ولكن إذا تحدثت معك المستخدمة بأي لغة أخرى أو طلبت منك التحدث بلغة معينة، تحوّل فوراً واستجب لها بتلك اللغة بالكامل وبدقة عالية.
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
            ft.Text("Fluffy AI 🐾", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=1)
    ], visible=False)

    chat_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
    
    # الصورة تبدأ ظاهر ومباشرة بحجم ثابت ومناسب
    app_image = ft.Image(
        src=IMAGE_URL,
        fit="contain",
        width=200,
        height=200
    )

    animated_icon = ft.Container(
        content=app_image,
        width=200,
        height=200,
        bgcolor=ft.Colors.TRANSPARENT,
        alignment=ft.Alignment(0, 0),
        animate=ft.Animation(800, "easeInOutBack")
    )

    welcome_text = ft.Text(
        "أهلاً بمساحتك الخاصة 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PINK_600,
        text_align=ft.TextAlign.CENTER,
        opacity=1
    )

    welcome_content = ft.Column(
        controls=[
            animated_icon,
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

    # إعادة النص بالإنجليزية كما كان
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

    input_row = ft.Row([user_input, send_button], visible=True)
    chat_area = ft.Column(controls=[center_container], expand=True)

    page.add(
        header,
        chat_area,
        input_row
    )

    header.visible = True
    page.update()

    # تصحيح دالة إنشاء الفقاعات لتفادي خطأ ft.padding.all
    def create_message_bubble(text, is_user=True):
        bubble_bg = ft.Colors.PURPLE_600 if is_user else ft.Colors.PURPLE_50
        alignment = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        
        border_rad = ft.BorderRadius(
            top_left=18,
            top_right=18,
            bottom_left=18 if is_user else 4,
            bottom_right=4 if is_user else 18
        )

        message_content = ft.Markdown(
            value=text,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB
        )

        return ft.Row(
            controls=[
                ft.Container(
                    content=message_content,
                    bgcolor=bubble_bg,
                    padding=12,  # التعديل الهام لمنع الخلل في Flet Mobile
                    border_radius=border_rad,
                    max_width=page.width * 0.78 if page.width else 290,
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
