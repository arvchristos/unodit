import os
import logging

try:
    # extension
    import pyuno_generator as pcg
    import config as conf

except ImportError:
    # command line
    import pythonpath.pyuno_generator as pcg
    import pythonpath.config as conf

IMPORT_DIR = conf.IMPORT_DIR


class CodeGenerator:
    """
    Generate code from uno context dict
    """

    def __init__(self, xdlfile, context, pydir='', app='MyApp', mode='script_convert', indent=4, **kwargs):
        self.xdlfile = xdlfile
        self.context = context
        self.pydir = pydir
        self.app = app
        self.mode = mode
        self.indent = indent
        self.kwargs = kwargs
        self.code = {}
        self.config = conf.ReadINI(conf.MAIN_DIR, self.pydir)
        self.SOURCE_DIR = self.config.get('directories', 'source_dir')
        self.logger = logging.getLogger('unodit.generator.CodeGenerator')
        self.logger.info('NEW LOGGER: unodit.generator.CodeGenerator')

    def generate_code(self):

        # convert
        if self.mode == 'script_convert' or self.mode == 'script_all':
            py_code = pcg.PythonGenerator(self.xdlfile, self.context, self.pydir, self.app, self.mode, self.indent)
            ui, logic = py_code.generate_py_code()
            self.write_app_exec_file(logic)
            self.write_main_ui_file(ui)

        # connect
        elif self.mode == 'connect':
            py_code = pcg.PythonGenerator(self.xdlfile, self.context, self.pydir, self.app, self.mode, self.indent)
            ui = py_code.generate_py_code()
            self.write_app_exec_file(ui)

        # embed
        elif self.mode == 'embed_convert' or self.mode == 'embed_all':
            py_code = pcg.PythonGenerator(self.xdlfile, self.context, self.pydir, self.app, self.mode, self.indent)
            ui = py_code.generate_py_code()
            self.write_app_exec_file(ui)

        # sidebar
        elif self.mode == 'sidebar_convert':
            py_code = pcg.PythonGenerator(self.xdlfile, self.context, self.pydir, self.app, self.mode, self.indent)
            ui, logic = py_code.generate_py_code()
            self.write_app_exec_file(logic)
            self.write_main_ui_file(ui)

    def write_main_ui_file(self, sui):
        """
        write generated python main ui file
        :param sui:
        """

        # if not exist create 'pythopath' dir
        if not os.path.exists(os.path.join(self.pydir, self.SOURCE_DIR, IMPORT_DIR)):
            os.makedirs(os.path.join(self.pydir, self.SOURCE_DIR, IMPORT_DIR))

        for name, value in self.kwargs.items():
            if name == 'panel_name':
                ui_file_name = value + self.config.get('ui_file', 'sufix') + '.py'
            else:
                ui_file_name = self.app + self.config.get('ui_file', 'sufix') + '.py'

        if self.mode == 'sidebar_convert':

            # if not exist create ui directory
            uidir = self.config.get('sdb_directories', 'sdb_ui')
            SDB_UI_DIR = os.path.join(self.pydir, self.SOURCE_DIR, IMPORT_DIR, uidir)
            if not os.path.exists(SDB_UI_DIR):
                os.makedirs(SDB_UI_DIR)

            # if the main ui file exists, remove it
            py_file_path = os.path.join(SDB_UI_DIR, ui_file_name)

        else:

            py_file_path = os.path.join(self.pydir, self.SOURCE_DIR, IMPORT_DIR, ui_file_name)

        # if the main ui file exists, remove it
        if os.path.exists(py_file_path):
            os.remove(py_file_path)

        py_main_ui_file = open(py_file_path, 'w')
        py_main_ui_file.write(sui)
        py_main_ui_file.close()

    def write_app_exec_file(self, lg):

        """
        write generated python app exec file

        :param lg:
        :return:
        """
        for name, value in self.kwargs.items():
            if name == 'panel_name':
                # same in sidebar.py
                exec_file_name = value + '.py'

                # if not exist create ui_logic directory
                uilogic = self.config.get('sdb_directories', 'sdb_ui_logic')
                SDB_LOGIC_DIR = os.path.join(self.pydir, self.SOURCE_DIR, IMPORT_DIR, uilogic)
                if not os.path.exists(SDB_LOGIC_DIR):
                    os.makedirs(SDB_LOGIC_DIR)

                py_file_path = os.path.join(SDB_LOGIC_DIR, exec_file_name)

            else:
                exec_file_name = self.app + '.py'
                py_file_path = os.path.join(self.pydir, self.SOURCE_DIR, exec_file_name)

        if not os.path.exists(self.pydir):
            os.makedirs(self.pydir)

        # source dir
        sdir = os.path.join(self.pydir, self.SOURCE_DIR)
        if not os.path.exists(sdir):
            os.makedirs(sdir)

        # if the logic file exists, do not remove it
        if os.path.exists(py_file_path):
            if os.path.isfile(py_file_path):
                pass
        else:
            py_main_ui_file = open(py_file_path, 'w')
            py_main_ui_file.write(lg)
            py_main_ui_file.close()
