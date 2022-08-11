class Upscale():
    def __init__(self, id = "0", status = "", file = ""):
        self.result = {}
        self.result["id"] = id
        self.result["status"] = status
        self.result["file"] = file

    def set_id(self, value: str):
        self.result["id"] = value

    def set_status(self, value: str):
        self.result["status"] = value

    def set_file(self, value: str):
        self.result["file"] = value

    def get_id(self):
        return self.result["id"]

    def get_status(self):
        return self.result["status"]

    def get_file(self):
        return self.result["file"]

    def get_data(self):
        return self.result
