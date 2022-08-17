# pylint: disable=invalid-name, undefined-variable, used-before-assignment
import os

Stage0 += comment(__doc__, reformat=False)

Stage0 += baseimage(image='docker://nvcr.io/nvidia/tensorflow:21.12-tf2-py3')

