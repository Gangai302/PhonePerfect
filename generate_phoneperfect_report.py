"""
PhonePerfect Project Report Generator
Constructs the complete PhonePerfect project report in DOCX following the exact template.
"""
import os
import shutil
import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

print("Starting PhonePerfect generator script setup...")
