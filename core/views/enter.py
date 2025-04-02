import flet as ft
from core.views.config import Styles
from core.models.user.user import User
from core.models.user.user_factory import UserFactory
from core.controller.logger import log
import traceback


class Enter:

    def __init__(
            self,
            page: ft.Page,
            user: User,
            update_view,
            update_listview,
            btn_logout,
            ):
        self.page = page
        self.user = user
        self.update_view = update_view
        self.update_listview = update_listview
        self.btn_logout = btn_logout

        self.username_field = ft.TextField(
            label="Username",
            bgcolor=Styles.BG_COLOR.value,
            border_color=Styles.BORDER_COLOR.value
            )
        
        self.login_password_field = ft.TextField(
            label="Password",
            bgcolor=Styles.BG_COLOR.value,
            border_color=Styles.BORDER_COLOR.value,
            password=True,
            can_reveal_password=True
        )

        self.login_error_text = ft.Text(color=Styles.ERROR_COLOR.value)

        self.login_view = ft.Container(
            content=ft.Column([
                self.username_field,
                self.login_password_field,
                self.login_error_text,
                ft.Row([
                    ft.Container(
                        content=ft.ElevatedButton(
                            'Log in',
                            on_click=self.login,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS),
                                text_style=ft.TextStyle(size=Styles.MIN_TEXT_SIZE),
                                elevation=10,
                                padding=ft.padding.all(10),
                            ),
                            expand=True
                        ),
                        width=200
                    ),
                    ft.Container(
                        content=ft.ElevatedButton(
                            'Register',
                            on_click=self.open_register,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS),
                                text_style=ft.TextStyle(size=Styles.MIN_TEXT_SIZE),
                                elevation=10,
                                padding=ft.padding.all(10)
                            ),
                            expand=True
                        ),
                        width=200
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            expand=True,
            alignment=ft.alignment.center,
            spacing=20,
            ),
            expand=True,
            margin=ft.margin.all(20),
            alignment=ft.alignment.center
        )

        self.username_register_field = ft.TextField(
            label="Username",
            bgcolor=Styles.BG_COLOR.value,
            border_color=Styles.BORDER_COLOR.value
        )

        self.password_register_field = ft.TextField(
            label="Password",
            bgcolor=Styles.BG_COLOR.value,
            border_color=Styles.BORDER_COLOR.value
        )

        self.register_view = ft.AlertDialog(
            content=ft.Column([
                self.username_register_field,
                self.password_register_field
            ],
            tight=True
            ),
            actions=[
                ft.TextButton('Close', on_click=self.close_register),
                ft.ElevatedButton(
                    'Submit',
                    on_click=self.register,
                    style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS.value)
                            )
                    )
            ]
        )

        self.page.overlay.append(self.register_view)
    
    
    def login(self, e):
        """
        Tries to login with the values on inputs, if the user
        exists then redirect to the main view, if not,
        says to user that the credentials are incorrect.
        """
        try:
            founded = self.user.login(
                username=self.username_field.value, 
                password=self.login_password_field.value
            )
            if isinstance(founded, tuple):
                self.user.state.change_user_state(user=self.user)
                self.user.set_id(founded[0])
                self.user.set_username(founded[1])
                self.user.set_password(founded[2])
                self.btn_logout.visible = True
                self.update_view()
                self.update_listview()
            else:
                self.login_error_text.value = 'Invalid username or password'
                self.login_error_text.update()
        except Exception:
            log(f'{__file__} - {traceback.format_exc()}')
    
    def register(self, e):
        """
        Tries to create a User with create function 
        that returns a boolean.
        Then, shows the user an alert if the user
        was created or not.
        """
        try:
            new_user = UserFactory.create(
                        username=self.username_register_field.value, 
                        value=self.password_register_field.value
                    )
            exists = new_user['user_exists']
            if exists == False:
                
                self.username_register_field.value = ''
                self.password_register_field.value = ''

                dialog = ft.AlertDialog(
                    title=ft.Text('User created successfully!')
                )
                self.page.dialog = dialog 
                dialog.open = True
                
                self.close_register(e)
                
                self.page.update()
            else:
                dialog = ft.AlertDialog(title=ft.Text('Cannot use these credentials'))
                self.page.dialog = dialog 
                dialog.open = True
                self.page.update()
        except Exception:
            log(f'{__file__} - {traceback.format_exc()}')

    def open_register(self, e):
        """
        In charge to open the register form
        """
        self.register_view.open = True
        self.page.update()

    def close_register(self, e):
        """
        It's called when the register form are correct
        or if the user want to close the register form
        """
        self.register_view.open = False
        self.page.update()