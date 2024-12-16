from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.renderers import JSONRenderer

__all__ = ["CustomRenderer"]



class CustomRenderer(JSONRenderer):
    """
    Custom renderer for managing API error responses.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = data

        if status.is_server_error(status_code) or status.is_client_error(status_code):
            response = self.check_errors(data)

        return super(CustomRenderer, self).render(
            response, accepted_media_type, renderer_context
        )

    def check_errors(self, data):
        global error_message
        if isinstance(data, dict):
            error_message = self.process_errors(data)
            if error_message:
                return {"errors": error_message, 'success': 'false'}
        elif isinstance(data, list):
            # Handle list of errors, for example, when bulk creating objects
            error_messages = []
            for item in data:
                if isinstance(item, dict):
                    error_message = self.process_errors(item)
                    if error_message:
                        return {"errors": "".join(error_message), 'success': 'false'}
                        # error_messages.append({"errors": error_message})
            if error_messages:
                return {"errors": "".join(error_message), 'success': 'false'}
        return {"errors": "".join(data), 'success': 'false'}
        # return data

    def process_errors(self, data, parent_key=''):
        for key, value in data.items():
            if isinstance(value, dict):
                nested_errors = self.process_errors(value, parent_key=key)
                if nested_errors:
                    return nested_errors  # Return the first error found

            elif isinstance(value, list):
                for error in value:
                    if isinstance(error, ErrorDetail):
                        field_name = key
                        if error.code == 'required':
                            if parent_key:
                                return f"{field_name} field is required in {parent_key}."
                            return f"{field_name} field is required."
                        elif error.code == 'unique' or error.code == 'invalid':
                            if parent_key:
                                return f"{error.rstrip('.')} in {parent_key}."
                            return str(error.rstrip("."))
                        else:
                            if parent_key:
                                return f"{error.rstrip('.')} for {field_name} in {parent_key}."
                            return str(error)

                    elif isinstance(error, dict):
                            nested_errors = self.process_errors(error, parent_key=key)
                            if nested_errors:
                                return nested_errors

                    else:
                        return self._get_type_error_message(item=error, parent_key=key)

            elif isinstance(value, str):
                return "".join(value)
        return None

    def _get_type_error_message(self, item, parent_key=''):
        """
        Helper method to get the error message for invalid type dynamically.
        """
        if isinstance(item, str):
            return f"Expected a list of items but got type \"str\" in {parent_key}."
        elif isinstance(item, int):
            return f"Expected a list of items but got type \"int\" in {parent_key}."
        elif isinstance(item, float):
            return f"Expected a list of items but got type \"float\" in {parent_key}."
        elif isinstance(item, dict):
            return f"Expected a list of items but got type \"dict\" in {parent_key}."
        elif isinstance(item, list):
            return f"Expected a list of items but got type \"list\" in {parent_key}."
        else:
            return f"Expected a list of items but got type \"{type(item).__name__}\" in {parent_key}."

