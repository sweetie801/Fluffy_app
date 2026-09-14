import flet as ft
from groq import Groq
import asyncio
import re

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# الرابط المباشر للصورة
IMAGE_URL = "https://i.postimg.cc/Vk7vpmxc/1000091096-removebg-preview.png"

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

# دالة فلترة وتصفية النماذج لضمان اختيار نموذج نصي يعمل مباشرة
def get_working_text_model():
    try:
        models_list = client.models.list()
        for model in models_list.data:
            model_id = model.id.lower()
            # استبعاد الصوت والأغراض الخاصة
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
    
    app_image = ft.Image(
        src=IMAGE_URL,
        fit="contain",
        width=280,
        height=280
    )

    animated_icon = ft.Container(
        content=app_image,
        width=280,
        height=280,
        bgcolor=ft.Colors.TRANSPARENT,
        alignment=ft.Alignment(0, 0),
        animate=ft.Animation(1000, "easeInOutBack")
    )

    welcome_text = ft.Text(
        "أهلاً بمساحتك الخاصة 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PINK_600,
        text_align=ft.TextAlign.CENTER,
        opacity=0,
        animate_opacity=ft.Animation(800, "easeIn")
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

    user_input = ft.TextField(
        hint_text="اكتبي رسالتك هنا...",
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

    # تأثير الحركة الترحيبية عند فتح التطبيق
    await asyncio.sleep(0.6)
    animated_icon.width = 140
    animated_icon.height = 140
    app_image.width = 140
    app_image.height = 140
    welcome_text.opacity = 1
    page.update()

    await asyncio.sleep(1.0)
    header.visible = True
    input_row.visible = True
    page.update()

    # دالة إنشاء فقاعة الرسالة التفاعلية
    def create_message_bubble(text, is_user=True):
        bubble_bg = ft.Colors.PURPLE_600 if is_user else ft.Colors.PURPLE_50
        text_color = ft.Colors.WHITE if is_user else ft.Colors.BLACK87
        alignment = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        
        # حواف دائرية تشبه فقاعات المحادثات
        border_rad = ft.BorderRadius(
            top_left=18,
            top_right=18,
            bottom_left=18 if is_user else 4,
            bottom_right=4 if is_user else 18
        )

        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(text, size=15, color=text_color, selectable=True),
                    bgcolor=bubble_bg,
                    padding=ft.padding.all(12),
                    border_radius=border_rad,
                    max_width=page.width * 0.75 if page.width else 280,
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

        # إضافة رسالتكِ كفقاعة على اليمين
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
        
        # إضافة رد Fluffy كفقاعة على اليسار
        chat_list.controls.append(create_message_bubble(fluffy_reply, is_user=False))
        
        send_button.disabled = False
        page.update()

    send_button.on_click = send_click
    user_input.on_submit = send_click

if __name__ == "__main__":
    ft.run(main)
