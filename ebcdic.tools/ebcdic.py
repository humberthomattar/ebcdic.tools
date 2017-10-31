# title           :ebcdic.py
# description     :Class responsavel por manter todos os metodos de manipulacao
# de arquivos EBCDIC
# author          :Humbertho Mattar
# date            :26/07/2017
# version         :0.1
# usage           :see readme.md
# notes           :see readme.md
# python_version  :2.7.6
# =======================================================================

from __future__ import with_statement
from tqdm import tqdm
import os
from contextlib import nested


class Ebcdic(object):

    def __init__(self, block_file, file_in):
        self.block_file = block_file
        self.file_in = file_in

    # Converte arquivo EBCDIC para ASCII
    def convert_to_ascii(self, pos_ini=0, pos_fim=None):
        if pos_fim is None:
            pos_fim = self.count_lines()
            total_bar = os.stat(self.file_in).st_size
        else:
            total_bar = (pos_fim - pos_ini) * self.block_file

        with tqdm(total=total_bar,
                  ncols=150, ascii=True,
                  desc=">>>> Convertendo arquivo") as pbar:
            file_out = self.file_in + "_ASCII.txt"
            with nested(open(self.file_in, 'rb'), open(file_out, 'wb\
            ')) as (infile, outfile):
                while pos_ini < pos_fim:
                    buffer = infile.read(self.block_file)
                    outfile.write(buffer.decode('cp500').encode(
                                                               'latin1')+'$\n')
                    pbar.update(self.block_file)
                    pos_ini += 1
        return

    # retorna numero inteiro do total de registros do arquivo
    def count_lines(self):
        return (int(os.stat(self.file_in).st_size) // self.block_file)

    # retorna um dicionario com todas as ocorrencias de uma string
    def find(self, fstring):
        total_lines = 0
        ocorrencias = {}
        with tqdm(total=os.stat(self.file_in).st_size,
                  ncols=150, ascii=True, esc=">>>> Pesquisando") as pbar:
            print('\n')
            with open(self.file_in, 'rb') as infile:
                while True:
                    buffer = infile.read(self.block_file).decode(
                                                      'cp500').encode('latin1')
                    if not buffer:
                        pbar.close()
                        break
                    if fstring in buffer:
                        ocorrencias[str(total_lines)] = buffer
                    total_lines += 1
                    pbar.update(self.block_file)
        return ocorrencias

    # retorna uma lista com o intervalo definido pos_ini e pos_fim
    def get_range(self, pos_ini, pos_fim):
        registros = []
        block_point = pos_ini * self.block_file
        with open(self.file_in, 'rb') as infile:
            infile.seek(block_point)
            while pos_ini <= pos_fim:
                buffer = infile.read(self.block_file).decode('cp500').encode(
                                                                      'latin1')
                registros.append(buffer)
                pos_ini += 1
        return registros

    # retorna uma lista com os primeiros registros (10 default)
    def head(self, head_range=10):
        registros = []
        with open(self.file_in, 'rb') as infile:
            for i in range(head_range):
                buffer = infile.read(self.block_file).decode('cp500').encode(
                                                                      'latin1')
                registros.append(buffer)
        return registros

    # retorna uma lista com os ultimos registros (10 default)
    def tail(self, tail_range=10):
        registros = []
        block_point = int(os.stat(self.file_in).st_size)
        block_point -= (self.block_file * tail_range)
        with open(self.file_in, 'rb') as infile:
            infile.seek(block_point)
            while True:
                buffer = infile.read(self.block_file).decode('cp500').encode(
                                                                      'latin1')
                if not buffer:
                    break
                registros.append(buffer)
        return registros
