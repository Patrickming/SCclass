import os
import shutil
import time
import pypinyin


class Students:
    STUDENT_NUMBER_INDEX = 0
    STUDENT_NAME_INDEX = 1
    STUDENT_GENDER_INDEX = 2
    STUDENT_CLASS_NUMBER_INDEX = 3
    STUDENT_GROUP_NUMBER_INDEX = 4

    def __init__(self):
        self.contracts_folder_name = "contracts"
        self.students_list = [
            ["2020131000", "张三", "M", "205", "1"],
            ["2021046067", "孙英苹", "M", "211", "1"],
            ["2021131001", "敬家好", "F", "211", "1"],
            ["2021131002", "黄文迪", "F", "211", "1"],
            ["2021131003", "徐圆梦", "F", "211", "1"],
            ["2021131004", "陈莉", "F", "211", "1"],
            ["2021131005", "何欣", "F", "211", "1"],
            ["2021131006", "江思颖", "F", "211", "1"],
            ["2021131007", "袁梓晴", "F", "211", "1"],
            ["2021131008", "罗欢", "F", "211", "1"],
            ["2021131009", "王宇航", "F", "211", "1"],
            ["2021131010", "张雨桐", "F", "211", "1"],
            ["2021131011", "王茜", "M", "211", "1"],
            ["2021131012", "陈炯颐", "M", "211", "1"],
            ["2021131013", "吴天宇", "M", "211", "1"],
            ["2021131014", "陈子天", "M", "211", "1"],
            ["2021131015", "高文杰", "M", "211", "1"],
            ["2021131016", "丁瑜清", "M", "211", "1"],
            ["2021131017", "白杰明", "M", "211", "1"],
            ["2021131018", "熊浩", "M", "211", "1"],
            ["2021131019", "梁家悦", "M", "211", "1"],
            ["2021131020", "邓景山", "M", "211", "1"],
            ["2021131021", "刘冠宇", "M", "211", "1"],
            ["2021131022", "尚龙泽", "M", "211", "1"],
            ["2021131023", "董青", "M", "211", "1"],
            ["2021131024", "周于超", "M", "211", "1"],
            ["2021131025", "辜锐彬", "M", "211", "1"],
            ["2021131026", "任豪", "M", "211", "1"],
            ["2021131027", "王晨", "M", "211", "1"],
            ["2021131028", "翁忠旭", "M", "211", "1"],
            ["2021131029", "毛思铖", "M", "211", "1"],
            ["2021131030", "关泓历", "M", "211", "1"],
            ["2021131031", "李金蒿", "M", "211", "1"],
            ["2021131032", "刘宇阳", "M", "211", "1"],
            ["2021131033", "康智豪", "M", "211", "1"],
            ["2021131034", "贾伟泽", "M", "211", "1"],
            ["2021131035", "蒋瑞", "M", "211", "1"],
            ["2021131036", "刘严", "M", "211", "1"],
            ["2021131037", "周正", "M", "211", "1"],
            ["2021131038", "张莘程", "M", "211", "1"],
            ["2021131039", "贾煜航", "M", "211", "1"],
            ["2021131040", "吴宏涛", "M", "211", "1"],
            ["2021131041", "崔博", "M", "211", "1"],
            ["2021131042", "杜以晴", "F", "212", "1"],
            ["2021131043", "刘杨", "F", "212", "1"],
            ["2021131044", "韦薪程", "F", "212", "1"],
            ["2021131045", "叶瑶瑶", "F", "212", "1"],
            ["2021131046", "杜彦霖", "F", "212", "1"],
            ["2021131047", "李宁", "F", "212", "1"],
            ["2021131048", "徐可", "F", "212", "1"],
            ["2021131049", "马应佳", "F", "212", "1"],
            ["2021131050", "张蕊", "F", "212", "1"],
            ["2021131051", "黄诗怡", "F", "212", "1"],
            ["2021131052", "刘鹏", "M", "212", "1"],
            ["2021131053", "吕梓桐", "M", "212", "1"],
            ["2021131054", "田文博", "M", "212", "1"],
            ["2021131055", "张宜斌", "M", "212", "1"],
            ["2021131056", "谷梓源", "M", "212", "1"],
            ["2021131057", "马得爽", "M", "212", "1"],
            ["2021131058", "马洋", "M", "212", "1"],
            ["2021131059", "田朝伟", "M", "212", "1"],
            ["2021131060", "廖卓", "M", "212", "1"],
            ["2021131061", "江鸿羽", "M", "212", "1"],
            ["2021131062", "孔令杰", "M", "212", "1"],
            ["2021131063", "朱奎镜", "M", "212", "1"],
            ["2021131064", "王议", "M", "212", "1"],
            ["2021131065", "谭弘琛", "M", "212", "1"],
            ["2021131066", "彭崚", "M", "212", "1"],
            ["2021131067", "冉乔", "M", "212", "1"],
            ["2021131068", "曾榆高", "M", "212", "1"],
            ["2021131069", "张笙", "M", "212", "1"],
            ["2021131070", "张子川", "M", "212", "1"],
            ["2021131071", "刘欢", "M", "212", "1"],
            ["2021131072", "李勇江", "M", "212", "1"],
            ["2021131074", "陈奕松", "M", "212", "1"],
            ["2021131075", "刘坤", "M", "212", "1"],
            ["2021131076", "刘培玮", "M", "212", "1"],
            ["2021131077", "程诗杰", "M", "212", "1"],
            ["2021131078", "缪志伟", "M", "212", "1"],
            ["2021131079", "张川", "M", "212", "1"],
            ["2021131080", "罗从文", "M", "212", "1"],
            ["2021131081", "许晨彬", "M", "212", "1"],
            ["2021131082", "母锏亓", "M", "212", "1"],
            ["2021122015", "黄志斌", "M", "213", "1"],
            ["2021131083", "李俊霜", "F", "213", "1"],
            ["2021131084", "韩乐瑶", "F", "213", "1"],
            ["2021131085", "尹何苹", "F", "213", "1"],
            ["2021131086", "郭延妍", "F", "213", "1"],
            ["2021131087", "陆冰玲", "F", "213", "1"],
            ["2021131088", "陈丽", "F", "213", "1"],
            ["2021131089", "肖潇", "F", "213", "1"],
            ["2021131090", "余宜芯", "F", "213", "1"],
            ["2021131091", "汪楠", "F", "213", "1"],
            ["2021131092", "彭敏", "M", "213", "1"],
            ["2021131094", "陈钦", "M", "213", "1"],
            ["2021131095", "李鑫", "M", "213", "1"],
            ["2021131096", "黎书义", "M", "213", "1"],
            ["2021131097", "蒋京育", "M", "213", "1"],
            ["2021131098", "王深源", "M", "213", "1"],
            ["2021131099", "聂思宇", "M", "213", "1"],
            ["2021131100", "蔡东", "M", "213", "1"],
            ["2021131101", "王语阳", "M", "213", "1"],
            ["2021131102", "张正阳", "M", "213", "1"],
            ["2021131103", "尹恒", "M", "213", "1"],
            ["2021131104", "罗嘉", "M", "213", "1"],
            ["2021131105", "彭郅崴", "M", "213", "1"],
            ["2021131106", "王宇佳", "M", "213", "1"],
            ["2021131107", "徐诚杰", "M", "213", "1"],
            ["2021131108", "韦科材", "M", "213", "1"],
            ["2021131109", "唐宏钦", "M", "213", "1"],
            ["2021131110", "陈华科", "M", "213", "1"],
            ["2021131112", "陈俊良", "M", "213", "1"],
            ["2021131113", "卢浩", "M", "213", "1"],
            ["2021131114", "席敬人", "M", "213", "1"],
            ["2021131115", "王栋", "M", "213", "1"],
            ["2021131116", "张昊宇", "M", "213", "1"],
            ["2021131117", "罗蘇瑞", "M", "213", "1"],
            ["2021131118", "何世言", "M", "213", "1"],
            ["2021131119", "刘俊余", "M", "213", "1"],
            ["2021131120", "陈思州", "M", "213", "1"],
            ["2021131121", "徐烜", "M", "213", "1"],
            ["2021131122", "陈祥福", "M", "213", "1"],
            ["2021131123", "李碧友", "M", "213", "1"],
            ["2021131124", "邢莎莎", "F", "214", "1"],
            ["2021131125", "钱奕蓉", "F", "214", "1"],
            ["2021131126", "熊灵欣", "F", "214", "1"],
            ["2021131127", "王一迪", "F", "214", "1"],
            ["2021131128", "黄培霞", "F", "214", "1"],
            ["2021131129", "杨雪", "F", "214", "1"],
            ["2021131130", "谭明月", "F", "214", "1"],
            ["2021131131", "曾炜傢", "F", "214", "1"],
            ["2021131132", "方妤心", "F", "214", "1"],
            ["2021131133", "虞子岳", "M", "214", "1"],
            ["2021131134", "陈凯祥", "M", "214", "1"],
            ["2021131135", "夏若茗", "M", "214", "1"],
            ["2021131136", "张佳伟", "M", "214", "1"],
            ["2021131137", "耿翔宇", "M", "214", "1"],
            ["2021131138", "刘骐宁", "M", "214", "1"],
            ["2021131139", "徐睿骐", "M", "214", "1"],
            ["2021131140", "曹梁", "M", "214", "1"],
            ["2021131141", "王乐", "M", "214", "1"],
            ["2021131142", "吴志帆", "M", "214", "1"],
            ["2021131143", "何玮俊", "M", "214", "1"],
            ["2021131144", "谢林希", "M", "214", "1"],
            ["2021131146", "祝子傑", "M", "214", "1"],
            ["2021131147", "雷明雨", "M", "214", "1"],
            ["2021131148", "汪南", "M", "214", "1"],
            ["2021131149", "黄彦童", "M", "214", "1"],
            ["2021131150", "孙杰", "M", "214", "1"],
            ["2021131151", "肖杰", "M", "214", "1"],
            ["2021131152", "刘家旗", "M", "214", "1"],
            ["2021131153", "谭子悦", "M", "214", "1"],
            ["2021131154", "祝宇", "M", "214", "1"],
            ["2021131155", "王星廷", "M", "214", "1"],
            ["2021131156", "常爻羽", "M", "214", "1"],
            ["2021131157", "何政伟", "M", "214", "1"],
            ["2021131158", "陈诺", "M", "214", "1"],
            ["2021131159", "张锭航", "M", "214", "1"],
            ["2021131160", "易孟", "M", "214", "1"],
            ["2021131161", "赵天宇", "M", "214", "1"],
            ["2021131162", "王予臻", "M", "214", "1"],
            ["2021131163", "向明达", "M", "214", "1"]
        ]

    def create_contract_folder(self):
        for student in self.students_list:
            time.sleep(0.1)
            folder_name = os.path.join("..", self.contracts_folder_name)
            folder_name = os.path.join(folder_name, student[Students.STUDENT_NUMBER_INDEX])

            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            file_name = os.path.join(folder_name, "HelloWorld.sol")

            if not os.path.exists(file_name):
                file = open(file_name, "a")
                file.write("// SPDX-License-Identifier: MIT\n")
                file.close()

            file_name = os.path.join(
                folder_name,
                "第1章作业-" + student[Students.STUDENT_NUMBER_INDEX] + ".txt")

            if not os.path.exists(file_name):
                folder_name_source = os.path.join("..", self.contracts_folder_name)
                folder_name_source = os.path.join(folder_name_source, "2020131000")
                file_name_source = os.path.join(folder_name_source, "第1章作业-2020131000.txt")
                # shutil.copyfile(file_name_source, file_name)

            file_name = os.path.join(
                folder_name,
                "第2章作业-" + student[Students.STUDENT_NUMBER_INDEX] + ".txt")

            if not os.path.exists(file_name):
                folder_name_source = os.path.join("..", self.contracts_folder_name)
                folder_name_source = os.path.join(folder_name_source, "2020131000")
                file_name_source = os.path.join(folder_name_source, "第2章作业-2020131000.txt")
                # shutil.copyfile(file_name_source, file_name)

    def get_name(self, student_index):
        name_chinese = self.students_list[student_index][Students.STUDENT_NAME_INDEX]
        return name_chinese

    def get_name_pinyin(self, student_index):
        name_chinese = self.students_list[student_index][Students.STUDENT_NAME_INDEX]
        word_pinyin_list = pypinyin.lazy_pinyin(name_chinese)
        word_pinyin_list_new = []

        for word_index in range(len(word_pinyin_list)):
            if 0 == word_index:
                word_new = word_pinyin_list[word_index][0].upper() + word_pinyin_list[word_index][1:]
            elif 1 == word_index:
                word_new = " " + word_pinyin_list[word_index][0].upper() + word_pinyin_list[word_index][1:]
            else:
                word_new = word_pinyin_list[word_index]

            word_pinyin_list_new.append(word_new)

        # for word_index in range(len(word_pinyin_list)):
        #     word_new = str(word_pinyin_list[word_index][0]).upper()
        #     for character_index in len(word_pinyin_list[word_index]):
        #         if character_index != 0:
        #             word_new = word_new + str(word_pinyin_list[word_index][character_index])
        #
        #     word_pinyin_list_new.append(str(word_pinyin_list[word_index][0]).upper())

        name_pinyin = ''.join(word_pinyin_list_new)

        return name_pinyin


if __name__ == "__main__":
    students = Students()
    students.create_contract_folder()
