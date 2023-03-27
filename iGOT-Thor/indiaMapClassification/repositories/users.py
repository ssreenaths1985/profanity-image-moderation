# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from indiaMapClassification.models import ICFModel


class ICFRepositories:

    @staticmethod
    def classify_image(image):
        result = ICFModel.classify_image(image)
        if result is None:
            return False
        return result
