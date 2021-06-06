import os


class YoctoBuildStatsGenerator:
    def __init__(self, sys_args):
        self.__check_parameters(sys_args)

    def parse(self, debug=False):
        if self.command == "name":
            return self.__command_get_packages_names()
        elif self.command == "configure":
            return self.__command_get_task_time("do_configure", debug)
        elif self.command == "compile":
            return self.__command_get_task_time("do_compile", debug)
        else:
            raise ValueError("Available commands:\nname\ntime")

    def __check_parameters(self, sys_args):
        if len(sys_args[1:]) != 2:
            raise ValueError("Usage: script [location] [command]")

        self.target_directory_path = os.path.abspath(sys_args[1])
        if not os.path.isdir(self.target_directory_path):
            raise ValueError(sys_args[1] + " is not a directory")
        self.command = sys_args[2]

    def __command_get_packages_names(self):
        print("Total: " + str(len(self.__get_subdir_names())))
        for sub_directory in self.__get_subdir_names():
            print(sub_directory)

    def __command_get_task_time(self, task, debug=False):
        print("Total: " + str(len(self.__get_subdir_names())))
        total_time = 0.0
        for sub_directory in self.__get_subdir_names():
            file_path = self.target_directory_path + "/" + sub_directory + "/" + task
            if os.path.isfile(file_path):
                if not debug:
                    time = self.__get_time_from_file(file_path)
                    total_time += float(time)
                    print(time)
                else:
                    time = self.__get_time_from_file(file_path)
                    total_time += float(time)
                    print(time + " " + sub_directory)
            else:
                if not debug:
                    print("-1")
                else:
                    print("-1 " + sub_directory)

        print("Total: " + str(len(self.__get_subdir_names())) + " packages")
        print("Total time: " + str(total_time))


    def __get_subdir_names(self):
        return [x[1] for x in os.walk(self.target_directory_path)][0]

    def __get_time_from_file(self, path):
        with open(path) as file:
            lines = file.readlines()
            return lines[3][14:-8]
