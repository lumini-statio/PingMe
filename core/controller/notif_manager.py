class NotificationManager:

    def __init__(self):
        self._observers = []


    def add_observer(self, observer):
        self._observers.append(observer)


    def notify_observers(self, message: str, username: str):
        for obs in self._observers:
            obs.send_notification(
                message=message,
                client_name=username
            )
