# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from textExtractionAndProfaneChecking.models import ICFModel


class ICFRepositories2:
    @staticmethod
    def upload_image1(image):
        result = ICFModel.upload_image1(image)
        if result is None:
            return False
        return result
