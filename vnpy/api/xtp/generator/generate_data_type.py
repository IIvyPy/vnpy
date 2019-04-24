""""""

TYPE_CPP2PY = {
    "int": "int",
    "char": "char",
    "double": "double",
    "short": "int",
    "uint8_t": "int",
    "enum": "enum"
}


class DataTypeGenerator:
    """DataType生成器"""

    def __init__(self, filename: str, prefix: str):
        """Constructor"""
        self.filename = filename
        self.prefix = prefix

        self.enum_count = 0

    def run(self):
        """主函数"""
        self.f_cpp = open(self.filename, "r", encoding="utf-8")
        self.f_define = open(f"{self.prefix}_constant.py", "w")
        self.f_typedef = open(f"{self.prefix}_typedef.py", "w")

        for line in self.f_cpp:
            self.process_line(line)

        self.f_cpp.close()
        self.f_define.close()
        self.f_typedef.close()

        print("DataType生成完毕")

    def process_line(self, line: str):
        """处理每行"""
        line = line.replace("\n", "")
        line = line.replace(";", "")

        if line.startswith("#define"):
            self.process_define(line)
        elif line.startswith("typedef"):
            if "enum" in line:
                self.process_enum_start(line)
            else:
                self.process_typedef(line)
        elif line.startswith("\tXTP_"):
            self.process_enum_body(line)

    def process_define(self, line: str):
        """处理常量定义"""
        words = line.split(" ")
        words = [word for word in words if word]
        if len(words) < 3:
            return

        name = words[1]
        value = words[2]

        new_line = f"{name} = {value}\n"
        self.f_define.write(new_line)

    def process_typedef(self, line: str):
        """处理类型定义"""
        words = line.split(" ")
        words = [word for word in words if word != " "]

        name = words[2]
        typedef = TYPE_CPP2PY[words[1]]

        if typedef == "char":
            if "[" in name:
                typedef = "string"
                name = name[:name.index("[")]

        new_line = f"{name} = \"{typedef}\"\n"
        self.f_typedef.write(new_line)
    
    def process_enum_start(self, line: str):
        """处理类型定义"""
        words = line.split(" ")
        words = [word for word in words if word != " "]

        name = words[2]
        new_line = f"{name} = \"enum\"\n"
        self.f_typedef.write(new_line)

        self.enum_count = 0
    
    def process_enum_body(self, line: str):
        """处理类型定义"""
        line = line.replace(",", "")
        line = line.replace("\t", " ")
        
        words = line.split(" ")
        words = [word for word in words if word]
        
        name = words[0]

        # 如果有enum初始值定义，则更新
        if "=" in words:
            self.enum_count = int(words[2])

        new_line = f"{name} = {self.enum_count}\n"
        self.f_define.write(new_line)

        self.enum_count += 1


if __name__ == "__main__":
    generator = DataTypeGenerator("../include/xtp/xtp_api_data_type.h", "xtp")
    generator.run()
