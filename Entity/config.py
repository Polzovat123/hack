
class ConfigValidator:
    def __init__(self, name_model):
            self.name_model = name_model


class ConfigIMG:
    def __init__(self, name_model, level_using):
        self.name_model = name_model
        self.level_using = level_using


class ConfigCompute:
    def __init__(self, level_detection, name_img_parser, level_using, name_validator):
        self.level_detection = level_detection
        self.config_img_parser = ConfigIMG(name_img_parser, level_using)
        self.config_validator = ConfigValidator(name_validator)