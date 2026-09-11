import flet as ft
from google import genai

def main(page: ft.Page):
    page.title = "Fluffy ✨"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # ضعي مفتاح API الخاص بك هنا
    client = genai.Client(api_key="ضعي_مفتاحك_هنا")

    output_text = ft.Text("مرحباً بكِ! اسأليني بما تحبين ✨", size=16)
    user_input = ft.TextField(label="اكتبي رسالتك هنا...", width=300)

    def send_click(e):
        if not user_input.value:
            return
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input.value,
            )
            output_text.value = response.text
        except Exception as ex:
            output_text.value = f"حدث خطأ: {ex}"
        page.update()

    send_button = ft.ElevatedButton("إرسال", on_click=send_click)

    page.add(
        ft.Column(
            [
                output_text,
                user_input,
                send_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
