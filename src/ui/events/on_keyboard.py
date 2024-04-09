def on_keyboard(window, key, *args):
    # Don't close application on ESC key
    if key == 27:
        return True