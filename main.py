import flet as ft
from groq import Groq

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

def main(page: ft.Page):
    page.title = "Fluffy Chat 🐾"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    chat_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    user_input = ft.TextField(
        hint_text="اكتبي رسالتك هنا...",
        expand=True,
        border_radius=20
    )

    def send_click(e):
        if not user_input.value.strip():
            return
            
        user_text = user_input.value
        chat_list.controls.append(
            ft.Text(f"أنت: {user_text}", size=16, weight=ft.FontWeight.BOLD)
        )
        user_input.value = ""
        page.update()

        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "أنت قط ذكي ولطيف اسمه Fluffy تجيب باللغة العربية بأسلوب مرح."},
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
        icon_color=ft.Colors.BLUE,
        on_click=send_click
    )

    page.add(
        ft.Text("مرحباً بك في Fluffy App 🐾", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        chat_list,
        ft.Row([user_input, send_button])
    )

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)
