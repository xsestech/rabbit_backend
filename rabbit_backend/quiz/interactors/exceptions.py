from rabbit_backend.quiz.entities import PublicObjectEntity


class PublicObjectAccessDeniedError(Exception):
    def __init__(self, public_object: PublicObjectEntity):
        object_name = type(public_object).__name__
        self.message = f"Access denied to {object_name} with id {public_object.id}"
        super().__init__(self.message)
