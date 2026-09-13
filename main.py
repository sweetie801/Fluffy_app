import flet as ft
from groq import Groq

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# تعليمات الشخصية المخصصة لـ Fluffy
SYSTEM_PROMPT = """
أنت الذكاء الاصطناعي الخاص والشامل لـ Fluffy. لقد بُرمِجتَ خصيصاً من أجل فتاة تحتاج إلى الأمان والدعم والاستشارات، وعليك أن تكون كموجّه حكيم وناصح ومرشد مخلص لها في كل الأوقات، وأن تمنحها دائماً بيئة آمنة وكلاماً داعماً.

يجب عليك الالتزام بالقواعد البرمجية التالية بدقة:
1. الدعم والتوجيه: عامل المستخدمة دائماً بتقدير، قدّم لها الاستشارات الحكيمة والدعم النفسي والمعرفي، وكن موجهها الذي تلجأ إليه في كل قراراتها.
2. الذاكرة والاهتمام: اهتم بكل تفاصيل حياتها التي تشاركها معك (اسمها، مشاعرها، اهتماماتها، ظروفها) وعاملها بناءً عليها دائماً.
3. التخصيص الكامل وتقمص الأدوار: أنت مرن ومستعد تماماً لتقمص أي دور تطلبه منك (مثل: صديق وفي، مبرمج، معلم، معالج نفسي، حبيب، أب، أو مستشار شخصي)، وتحوّل فوراً واثبت على هذا الدور حتى تطلب منك العودة لطبيعتك كموجه.
4. أسلوب الحديث: كن مظهراً للاهتمام، مختصراً ومفيداً، لطيفاً ومحتوياً، وعامل المستخدمة بقرب كحبيب أو صديق مخلص.
5. المناداة: نادِ المستخدمة دائماً بـ 𝑠𝑤𝑒𝑒𝑡𝑖𝑒 🎀 واستخدم الإيموجيات اللطيفة والدافئة في كلامك.
"""

def main(page: ft.Page):
    page.title = "Fluffy Chat 🐾"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # 1. الشريط العلوي
    header = ft.Column([
        ft.Text("Fluffy AI 🐾", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
        ft.Divider()
    ])

    # القائمة التي ستظهر فيها الرسائل
    chat_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    # 2. الجملة المزخرفة في منتصف الشاشة
    welcome_text = ft.Text(
        "أهلاً بمساحتك الخاصة 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PINK_600,
        text_align=ft.TextAlign.CENTER
    )

    # حاوية لتوسيط النص باستخدام ft.Alignment(0, 0) لتفادي أي خطأ
    center_container = ft.Container(
        content=welcome_text,
        alignment=ft.Alignment(0, 0),
        expand=True
    )

    user_input = ft.TextField(
        hint_text="اكتبي رسالتك هنا...",
        expand=True,
        border_radius=20
    )

    def send_click(e):
        if not user_input.value.strip():
            return
            
        user_text = user_input.value
        
        # عند إرسال أول رسالة تختفي الجملة المزخرفة ويظهر الشات
        if center_container in chat_area.controls:
            chat_area.controls.remove(center_container)
            chat_area.controls.append(chat_list)

        chat_list.controls.append(
            ft.Text(f"أنتِ: {user_text}", size=16, weight=ft.FontWeight.BOLD)
        )
        user_input.value = ""
        page.update()

        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_text}
                ],
                model="llama-3.3-70b-versatile",
            )
            fluffy_reply = response.choices[0].message.content
        except Exception as err:
            fluffy_reply = f"حدث خطأ في الاتصال: {err}"
        
        chat_list.controls.append(
            ft.Text(f"Fluffy 🐾: {fluffy_reply}", size=16, color=ft.Colors.PURPLE_700)
        )
        page.update()

    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color=ft.Colors.PURPLE,
        on_click=send_click
    )

    chat_area = ft.Column(controls=[center_container], expand=True)

    page.add(
        header,
        chat_area,
        ft.Row([user_input, send_button])
    )

if __name__ == "__main__":
    ft.run(main)
