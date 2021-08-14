import glob
import logging
import os.path
import re
from enum import Enum, unique
from functools import reduce

import docker


@unique
class FileType(Enum):

    def __init__(self, suffix: list):
        self.suffix = suffix

    Pdf = ["pdf"]
    Epub = ["epub"]
    Markdown = ["md"]
    Html = ["html", "htm"]

    @staticmethod
    def value_of(file_type):
        if isinstance(file_type, str):
            file_type = file_type.lower()
            for name, member in FileType.__members__.items():
                if str(name).lower() == file_type:
                    return member
            else:
                raise ValueError(f"'{FileType.__name__}' enum not found for '{file_type}'")
        if isinstance(file_type, FileType):
            return file_type

    def __str__(self):
        return self.name


class Command:
    CONTAINER_WORKING_DIR = "/data"

    def __init__(self, input_format=FileType.Html):
        self._input_format = FileType.value_of(input_format)

    @staticmethod
    def pdf(i: str, o: str):
        PdfMaker(i, os.path.basename(o)).run()

    @staticmethod
    def epub():
        pass


class PdfMaker:

    def __init__(self, source_path, target_name, input_format=FileType.Html) -> None:
        self._source_path = os.path.realpath(source_path)
        self._target_name = target_name
        self._input_format = input_format
        self.work_dir = f"/data/{self._input_format}"
        self.is_folder = True if os.path.isdir(self._source_path) else False

    def run(self):
        file_list = self._get_specially_files()
        logging.info(file_list)
        client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
        run_command = f"-f {self._input_format} \
                                --pdf-engine=xelatex --toc \
                                --highlight-style tango \
                                -V colorlinks -V urlcolor=NavyBlue -V toccolor=NavyBlue \
                                -V 'mainfont:FZShuSong-Z01S' \
                                -s -o {self._get_target()} \
                                {self._get_head_tex()} \
                                --resource-path {self._get_resource_path()} \
                                {file_list}"
        print(run_command)
        client.containers.run(image="5200710/pandoc-latex:latest",
                              command=run_command, remove=True,
                              volumes=self._get_volumes(),
                              working_dir=self.work_dir)

    def _get_specially_files(self) -> list:
        if not os.path.exists(self._source_path):
            raise FileExistsError(f"{self._source_path} not exists")
        if self.is_folder:
            file_name_list = self._parse_file_name_list_from_toc_md()
            if not file_name_list:
                glob_express_list = map(lambda suffix: glob.glob(os.path.join(self._source_path, f'*.{suffix}')),
                                        self._input_format.suffix)
                file_name_list = sorted(map(os.path.basename, reduce(lambda a, b: a + b, glob_express_list)))
            basename = os.path.basename(self._source_path)
            file_list = map(lambda filename: os.path.join(basename, filename), file_name_list)
        else:
            if not os.path.splitext(self._source_path)[-1] in self._input_format.suffix:
                logging.warning(f"{os.path.splitext(self._source_path)[-1]} not in the suffix {self._input_format.suffix}")
            file_list = [os.path.basename(self._source_path)]
        return " ".join(map(lambda x: f"\'{x}\'", file_list))

    def _get_volumes(self) -> dict:
        dirname = os.path.dirname(self._source_path)
        return {dirname: {'bind': f'{self.work_dir}', 'mode': 'rw'}}

    def _get_resource_path(self):
        if self.is_folder:
            folder_name = os.path.basename(self._source_path)
            return os.path.join(self.work_dir, folder_name)
        return self.work_dir

    def _get_target(self):
        return os.path.join(self.work_dir, self._target_name)

    def _parse_file_name_list_from_toc_md(self):
        toc_path = os.path.join(self._source_path, "toc.md")
        content_list = []
        if os.path.exists(toc_path) and os.path.isfile(toc_path):
            with open(toc_path, "r", encoding='utf-8') as f:
                for line in f.readlines():
                    m = re.match(r"^\s*#{1,3}\s+(.*)\s*", str(line))
                    if m:
                        content_list.append(m.group(1))

        file_name_list = []
        for name in content_list:
            for suffix in self._input_format.suffix:
                file_name = f"{name}.{suffix}"
                if os.path.exists(os.path.join(self._source_path, file_name)):
                    file_name_list.append(file_name)

        return file_name_list

    def _get_head_tex(self) -> str:
        head_tex = os.path.join(os.path.dirname(self._source_path), "head.tex")
        if os.path.exists(head_tex):
            return f'-H {os.path.join(self.work_dir, "head.tex")}'
        return ""


if __name__ == '__main__':
    # print(FileType.Pdf)
    # fire.Fire(Command)
    Command().pdf("../ebook/Kafka核心技术与实战", "output/index.pdf")
