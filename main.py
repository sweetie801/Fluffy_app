import flet as ft
from google import genai

def main(page: ft.Page):
    page.title = "Fluffy AI Companion"
    page.vertical_alignment = ft.MainAxisAlignment.END
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # مفتاحكِ الحقيقي الذي قمتِ بإرساله
    client = genai.Client(api_key="AQ.Ab8RN6J9pjs9dwaMlBlm0LoItfzd0tP2mV0_ZVp9WlVNJtUltg")

    chat = ft.ListView(expand=1, spacing=10, auto_scroll=True)

    def send_click(e):
        if not new_message.value:
            return

        user_text = new_message.value
        new_message.value = ""

        chat.controls.append(ft.Text(f"أنت: {user_text}"))
        page.update()

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_text
            )
            bot_text = response.text
            chat.controls.append(ft.Text(f"Fluffy: {bot_text}"))
            
        except Exception as err:
            chat.controls.append(ft.Text(f"خطأ: {err}"))

        page.update()

    new_message = ft.TextField(
        hint_text="اكتبي رسالتك هنا...",
        expand=True,
        border_radius=20,
        filled=True,
        on_submit=send_click
    )

    send_button = ft.ElevatedButton("إرسال", on_click=send_click)

    page.add(
        chat,
        ft.Row([new_message, send_button])
    )

ft.app(target=main)
