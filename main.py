import flet as ft
from google import genai

def main(page: ft.Page):
    page.title = "Fluffy ✨"
    page.theme_mode = ft.ThemeMode.DARK
    page.rtl = True

    chat = ft.ListView(expand=True, spacing=10, padding=10)
    new_message = ft.TextField(
        hint_text="اكتبي رسالتك هنا...",
        expand=True,
        border_radius=20,
        filled=True,
        on_submit=lambda e: send_click(None)
    )
    
    history = []
    
    # ضعي مفتاح API الخاص بك هنا
    client = genai.Client(api_key="ضعي_مفتاحك_هنا")

    def send_click(e):
        if not new_message.value:
            return
        
        user_text = new_message.value
        new_message.value = ""
        
        chat.controls.append(ft.Text(f"أنتِ: {user_text}", color=ft.colors.PINK_300))
        page.update()

        history.append({"role": "user", "parts": [user_text]})

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=history,
            )
            bot_text = response.text
            chat.controls.append(ft.Text(f"Fluffy ✨: {bot_text}", color=ft.colors.PURPLE_300))
            history.append({"role": "model", "parts": [bot_text]})
        except Exception as err:
            chat.controls.append(ft.Text(f"خطأ: {str(err)}", color=ft.colors.RED_400))
            
        page.update()

    page.add(
        ft.Row(
            [ft.Text("Fluffy ✨ AI Companion", size=18, weight="bold")],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        chat,
        ft.Row([
            new_message, 
            ft.ElevatedButton("إرسال", on_click=send_click)
        ])
    )

ft.app(target=main)
