import flet as ft
from CustomLibs import cache_parsing

def main(page: ft.Page):
    # functions
    def get_cache_dir(e: ft.FilePickerResultEvent):
        if e.path:
            t_cache_dir.value = e.path
            t_cache_dir.update()
        else:
            "Cancelled"
        return 0

    def get_output_dir(e: ft.FilePickerResultEvent):
        if e.path:
            t_output_dir.value = e.path
            t_output_dir.update()
        else:
            "Cancelled"
        return 0

    def open_dlg_progress():
        page.dialog = dlg_progress
        dlg_progress.open = True
        page.update()

    def close_dlg_progress(e):
        page.window_prevent_close = False
        dlg_progress.open = False
        page.update()

    def input_validation(cbox_list):
        page.dialog = dlg_error
        if t_cache_dir.value is None or t_cache_dir.value == "":
            dlg_error.content = ft.Text("No cache directory chosen.")
            dlg_error.open = True
            page.update()
            return False
        elif t_output_dir.value is None or t_output_dir.value == "":
            dlg_error.content = ft.Text("No output directory chosen.")
            dlg_error.open = True
            page.update()
            return False

        for cbox in cbox_list:
            if cbox.value:
                return True
        dlg_error.content = ft.Text("No file types chosen.")
        dlg_error.open = True
        page.update()
        return False

    def switch_all(e):
        if switch_all.value:
            for checkbox in checkbox_list:
                checkbox.value = True
                checkbox.update()
        else:
            for checkbox in checkbox_list:
                checkbox.value = False
                checkbox.update()

    def switch_images(e):
        image_list = [c_jpg, c_png, c_gif, c_webp]
        if switch_images.value:
            for checkbox in image_list:
                checkbox.value = True
                checkbox.update()
        else:
            for checkbox in image_list:
                checkbox.value = False
                checkbox.update()

    def switch_videos(e):
        video_list = [c_mp4, c_mov, c_webm]
        if switch_videos.value:
            for checkbox in video_list:
                checkbox.value = True
                checkbox.update()
        else:
            for checkbox in video_list:
                checkbox.value = False
                checkbox.update()

    def switch_archives(e):
        archive_list = [c_woff2, c_gz, c_rar, c_zip, c_7z, c_bz2]
        if switch_archives.value:
            for checkbox in archive_list:
                checkbox.value = True
                checkbox.update()
        else:
            for checkbox in archive_list:
                checkbox.value = False
                checkbox.update()

    def parse_cache(cache_dir, output_dir):
        # initialize type list
        type_list = []

        if input_validation(checkbox_list):
            # open loading dialog
            page.window_prevent_close = True
            open_dlg_progress()
            page.update()

            # add selected extensions to type list
            for checkbox in checkbox_list:
                if checkbox.value:
                    type_list.append(checkbox.label.lower())

            cache_parsing.main(cache_dir, output_dir, type_list)

            # close loading dialog
            close_dlg_progress(e=None)
            page.update()

    # page settings
    page.title = "CacheGrab"

    # dialogues
    dlg_pick_cache_dir = ft.FilePicker(on_result=get_cache_dir)
    dlg_pick_output_dir = ft.FilePicker(on_result=get_output_dir)
    dlg_progress = ft.AlertDialog(title=ft.Text("Extracting"),
                                  content=ft.ProgressRing(width=25, height=25, stroke_width=2),
                                  actions=[ft.TextButton("Stop Extraction", on_click=close_dlg_progress)],
                                  actions_alignment=ft.MainAxisAlignment.CENTER,
                                  modal=True)
    dlg_error = ft.AlertDialog(title=ft.Text("Error"))
    page.overlay.append(dlg_pick_cache_dir)
    page.overlay.append(dlg_pick_output_dir)

    # text fields
    t_cache_dir = ft.TextField(label="Cache Directory", read_only=True)
    t_output_dir = ft.TextField(label="Output Directory", read_only=True)

    # buttons
    b_extract = ft.ElevatedButton(
        text="Extract",
        on_click=lambda _: parse_cache(t_cache_dir.value, t_output_dir.value),
        height=50, width=150
    )
    b_cache_dir = ft.ElevatedButton(
        text="Select Cache Dir",
        on_click=lambda _: dlg_pick_cache_dir.get_directory_path(),
        height=50
    )
    b_output_dir = ft.ElevatedButton(
        text="Select Output Dir",
        on_click=lambda _: dlg_pick_output_dir.get_directory_path(),
        height=50
    )

    # checkboxes
    c_jpg = ft.Checkbox(label="JPG")
    c_png = ft.Checkbox(label="PNG")
    c_gif = ft.Checkbox(label="GIF")
    c_webp = ft.Checkbox(label="WEBP")
    c_mp4 = ft.Checkbox(label="MP4")
    c_mov = ft.Checkbox(label="MOV")
    c_webm = ft.Checkbox(label="WEBM")
    c_woff2 = ft.Checkbox(label="WOFF2")
    c_gz = ft.Checkbox(label="GZ")
    c_rar = ft.Checkbox(label="RAR")
    c_zip = ft.Checkbox(label="ZIP")
    c_7z = ft.Checkbox(label="7Z")
    c_bz2 = ft.Checkbox(label="BZ2")

    checkbox_list = [c_jpg, c_png, c_gif, c_webp, c_mp4, c_mov, c_webm, c_woff2, c_gz, c_rar, c_zip, c_7z, c_bz2]

    # switches
    switch_all = ft.Switch(label="All", on_change=switch_all)
    switch_images = ft.Switch(label="Images", on_change=switch_images)
    switch_videos = ft.Switch(label="Videos", on_change=switch_videos)
    switch_archives = ft.Switch(label="Archives", on_change=switch_archives)

    # page display
    page.add(
        ft.Column([
            ft.Row([
                ft.Text("CacheGrab", size=40)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(padding=20),
            ft.Row([
                t_cache_dir, b_cache_dir
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                t_output_dir, b_output_dir
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                c_jpg, c_png, c_gif, c_webp, c_mp4, c_mov, c_webm
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                c_woff2, c_gz, c_rar, c_zip, c_7z, c_bz2
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                switch_videos, switch_images, switch_archives, switch_all
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                b_extract
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True, alignment=ft.MainAxisAlignment.CENTER)
    )


# run the program
ft.app(target=main)
