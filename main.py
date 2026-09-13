import flet as ft
from groq import Groq

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

def main(page: ft.Page):
    page.title = "Fluffy Chat 🐾"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # 1. الشريط العلوي ثابت في الأعلى دائماً
    header = ft.Column([
        ft.Text("Fluffy App 🐾", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
        ft.Divider()
    ])

    # القائمة التي ستظهر فيها الرسائل بعد إرسالها
    chat_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    # 2. الجملة المزخرفة في منتصف الشاشة
    welcome_text = ft.Text(
        "أهلاً بمساحتك الخاصة 𝑆𝑤𝑒𝑒𝑡𝑖𝑒 🎀",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PINK_600,
        text_align=ft.TextAlign.CENTER
    )

    # حاوية لتوسيط النص
    center_container = ft.Container(
        content=welcome_text,
        alignment=ft.alignment.center,
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
                    {"role": "system", "content": "أنت قط ذكي ولطيف اسمه Fluffy تجيب باللغة العربية بأسلوب مرح ودود."},
                    {"role": "user", "content": user_text}
                ],
                model="llama-3.3-70b-versatile",
            )
            fluffy_reply = response.choices[0].message.content
        except Exception as err:
            fluffy_reply = f"حدث خطأ في الاتصال: {err}"
        
        chat_list.controls.append(
            ft.Text(f"Fluffy 🐾: {fluffy_reply}", size=16, color=ft.Colors.BLUE_700)
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
