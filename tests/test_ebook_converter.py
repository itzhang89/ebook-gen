import pytest

from ebook_gen.ebook_converter import Command, FileType


@pytest.fixture(scope='class')
def input_path():
    return "tests/resources/input_path"


@pytest.fixture
def command() -> Command:
    return Command()


class TestCommand:

    def test_input_file_would_be_empty_when_input_empty_folder(self, command, tmpdir):
        command.pdf(tmpdir)
        assert len(command._input_file_list) == 0

    @pytest.mark.parametrize("input_format,length_size", [(FileType.Pdf, 2), (FileType.Html, 3)])
    def test_return_specially_type_file_list_with_sorted_by_dict(self, command, input_format, length_size):
        input_path = 'input_path'
        command._input_format = input_format

        command.pdf(input_path)

        assert len(command._input_file_list) == length_size

    def test_should_raise_exception_when_input_file_path_not_existed(self, command):
        input_path = 'tests/input_path/not_existed'
        with pytest.raises(FileExistsError):
            command.pdf(input_path)
