class Credentials(object):
    def __init__(self, credentials):
        if credentials is None:
            raise TypeError("A 'credentials' object must be provided")
        else:
            try:
                # Make the assumption that the object passed in has both "username" & "password" attributes/properties
                self._username = credentials.username
                self._password = credentials.password
            except AttributeError:
                raise TypeError("An invalid 'credentials' object was provided")

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password
