import flet as ft
from config import Styles
from core.models.user.user import User
from core.models.user.user_factory import UserFactory
from core.models.models import UserModel
from core.controller.utils.logger import log, async_log


@log
def auth_view(page: ft.Page, user: User, update_view):
    username_field = ft.TextField(
        label="Username",
        bgcolor=Styles.BG_COLOR.value,
        border_color=Styles.BORDER_COLOR
    )
    
    login_password_field = ft.TextField(
        label="Password",
        bgcolor=Styles.BG_COLOR.value,
        border_color=Styles.BORDER_COLOR,
        password=True,
        can_reveal_password=True
    )

    login_error_text = ft.Text(
        color=Styles.ERROR_COLOR.value,
        size=Styles.MIN_TEXT_SIZE.value,
        style=ft.TextStyle(weight=ft.FontWeight.BOLD)
    )

    username_register_field = ft.TextField(
        label="Username",
        bgcolor=Styles.BG_COLOR,
        border_color=Styles.BORDER_COLOR
    )

    password_register_field = ft.TextField(
        label="Password",
        bgcolor=Styles.BG_COLOR,
        border_color=Styles.BORDER_COLOR,
        password=True,
        can_reveal_password=True
    )

    register_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Register new account"),
        content=ft.Column([username_register_field, password_register_field], tight=True),
        actions=[
            ft.TextButton('Close', on_click=lambda e: toggle_register(False)),
            ft.ElevatedButton('Submit', on_click=lambda e: _handle_register(e))
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )


    @async_log
    async def login(e):
        result = user.login(
            username=username_field.value, 
            password=login_password_field.value
        )

        if result and isinstance(result[0], tuple):
            user_founded = result[0]
            user.state.change_user_state(user=user)
            user.id = user_founded[0]
            user.username = user_founded[1]
            user.password = user_founded[2]
            await update_view()
        else:
            login_error_text.value = 'Invalid username or password'
            await login_error_text.update_async()

    btn_register = ft.ElevatedButton(
        'Submit',
        on_click=lambda e: _handle_register(e),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS.value)
        )
    )

    @async_log
    async def _perform_register():
        if username_register_field.value and password_register_field.value:

            if UserModel.select().where(UserModel.username == username_register_field.value).exists():

                dialog = ft.AlertDialog(title=ft.Text('Cannot use these credentials'))
                page.dialog = dialog 
                dialog.open = True
                page.update()

            else:
            
                UserFactory.create(
                    username=username_register_field.value, 
                    value=password_register_field.value
                )

                dialog = ft.AlertDialog(
                    title=ft.Text('User created successfully!')
                )
                
                username_register_field.value = ''
                password_register_field.value = ''

                page.dialog = dialog 
                dialog.open = True

                await page.update_async()


    @log
    def _handle_register(e):
        page.run_task(_perform_register)


    register_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Register new account"),
        content=ft.Column([
            username_register_field,
            password_register_field
        ], tight=True),
        actions=[
            ft.TextButton(
                'Close',
                on_click=lambda e: toggle_register(False), 
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS))
                ),
            btn_register
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    @log
    def toggle_register(open: bool):
        register_dialog.open = open
        page.update()


    return {
        "view": ft.Container(
            content=ft.Column([
                username_field,
                login_password_field,
                login_error_text,
                ft.Row([
                    ft.ElevatedButton(
                        'Log in',
                        on_click=login,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS.value),
                            padding=ft.padding.only(left=30, right=30)
                        )
                    ),
                    ft.ElevatedButton(
                        'Register',
                        on_click=lambda e: toggle_register(True),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS.value),
                            padding=ft.padding.only(left=25, right=25)
                        )
                        ),
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], expand=True, alignment=ft.MainAxisAlignment.CENTER),
            expand=True,
            margin=ft.margin.all(20)
        ),
        "dialog": register_dialog
    }
