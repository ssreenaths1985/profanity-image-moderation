# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from imageClassifier.models import ICFModel


class ICFRepositories:

    @staticmethod
    def upload_image1(image):
        result = ICFModel.upload_image1(image)
        if result is None:
            return False
        return result
