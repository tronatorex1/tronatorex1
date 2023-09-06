#!/usr/bin/env python3
###################################################################################################
#   IN SPANISH
#   1 Lee los argumentos pasados por el usuario para determinar: nombre del tgz, máscara de archivos
#     deseados a buscar, retención (antigüedad) de los archivos, path o ruta dónde encontrarlos
#   2 Procede a ejecutar a nivel de linux, comandos "find" y "tar" para así usar la misma metodología
#     que el proceso homólogo "housekeeping.sh", dejando toda la tarea a manos del S.O. linux
#   3 Una vez ejecutados los tar/compresion y el borrado de los archivos ya comprimidos, en la ruta
#     deseada, se guarda un log file minimalista (sólo indica fecha y hora de cada ejecución, así para
#     que el housekeeping se convierta en otro proceso que consume espacio en el FS dónde se decida
#     desplegar
#
#   Cómo ejecutar?
#   > python* <this.py> -f "<nombre tgz>" -p "<ruta>"        -e "<máscara selec.>" -r "<ret. (días)>"
#                       -f "tar_gzip"     -p "/ine/scripts/" -e "*.txt"            -r "5"
#   * usar python3 en linux, python en windows
#   CurrUsr: None
####################################################################################################

import sys, os, subprocess, getopt, datetime, tarfile

# variables
out_file_ = log_file = ext_ = ret_ = path_ = ""
files = []
argv = sys.argv[1:]
date_ = datetime.datetime.now().strftime("%Y%m%d_%H%M")


# Use the following lines to use interactive getOps in CMD
try:
    opts, args = getopt.getopt(argv, ":f:p:e:r:")
except:
    print("--Error: opcion invalida! Usar solamente -f=\"tgz output file\" -e=\"mascara de archivos deseados\" -r=\"retencion/antiguiedad deseada\" -p=\"ruta de dataset\" ; -h=help")

for opt, arg in opts:
    if opt in ['-f']:
        out_file_ = arg
    if opt in ['-p']:
        path_ = arg
    if opt in ['-e']:
        ext_ = arg
    if opt in ['-r']:
        ret_ = arg

log_file = "log_housekeeping.log"

print(f"\n **Housekeeping (generico){chr(10)}    Proceso de compresion de archivos locales y borrado")
print(f"    Extension:    {ext_}")
print(f"    Retencion:    {ret_} dia(s)\n")

# 1 log file: no entry (o)
with open(log_file, "a") as f:
    # 2 list objective files and taring desired files and removing files
    stmt_to_exec=f'tar -cvpzf "{path_}{out_file_}_{date_}.tgz" `find "{path_}" -maxdepth 1 -type f -iname "{ext_}" -mtime +"{ret_}"` && find "{path_}" -maxdepth 1 -type f -iname "{ext_}" -mtime "+{ret_}" -print0 | xargs -0 rm -f'
    cmd = subprocess.Popen(stmt_to_exec, shell=True, close_fds=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    cmd.wait()
    while cmd.poll() is None:
        time.sleep(0.5)  # Process hasn't exited yet, let's wait some time more, as a double check
    ret_code = cmd.returncode
    ret_msg = cmd.communicate()[0]
    print(f"    ==> Res: {ret_code}{chr(10)}{ret_msg}")

    # 3 close and log file: entry (f)
    date_ = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    f.write(f'{date_}    -> Fin del housekeeping! Revisar los archivos generados/borrados localmente [ {path_}{out_file_}_{date_}.tgz ]{chr(10)}')
    print(f"    -> Fin del housekeeping! Revisar los archivos generados/borrados localmente{chr(10)}")