# -*- coding: utf-8 -*-
db.define_table('theme',
                Field('theme_name'))

db.define_table('sub_theme',
                Field('sub_theme_name'),
                Field('theme', 'reference theme')
                )

db.define_table('lego_set',
                Field('set_number'),
                Field('set_name'),
                Field('piece_count'),
                Field('minifig_count'),
                Field('year_released'),
                Field('theme', 'reference theme'),
                Field('sub_theme', 'reference sub_theme')
                )
