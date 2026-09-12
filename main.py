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
