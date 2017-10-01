{
  'variables': {
    'platform': '<(OS)',
  },
  'conditions': [
    # Replace gyp platform with node platform, blech
    ['platform == "mac"', {'variables': {
      'platform': 'darwin',
      'ANTTWEAKBAR_ROOT': '/usr/local/Cellar/anttweakbar/1.16',
    }}],
    ['platform == "win"', {'variables': {'platform': 'win32'}}],
  ],
  'targets': [
    {
      'target_name': 'copy_libs',
      'type': 'none',
      'copies': [
        {
          'destination': '<(module_root_dir)/build/Release/',
          'files': [
            '<(module_root_dir)/deps/windows/dll/AntTweakBar.dll',
            '<(module_root_dir)/deps/windows/dll/AntTweakBar64.dll',
            '<(module_root_dir)/deps/windows/dll/FreeImage.dll',
            '<(module_root_dir)/deps/windows/dll/glew32.dll',
            '<(module_root_dir)/deps/windows/dll/glfw3.dll'
          ]
        }
      ]
    },
    {
      'target_name': 'glfw',
      'defines': [
        'VERSION=0.4.6',
      ],
      'sources': [
        'src/atb.cc',
        'src/glfw.cc'
      ],
      'include_dirs': [
        "<!(node -e \"require('nan')\")",
        './deps/include',
      ],
      'conditions': [
        ['OS=="linux"', {
          'include_dirs': [
            "/usr/local/include",
            './deps/include',
            "/usr/include/X11"
          ],
          'library_dirs': [
              "./deps/linux/lib",
              "/usr/include/GL",
              "/usr/local/lib/",
              "/usr/lib/i386-linux-gnu",
              "./deps/linux/lib/<(target_arch)",
              ],
          'libraries': [
            '-lAntTweakBar', '<!@(pkg-config --libs glfw3 glew)',
            '-lXrandr','-lXinerama','-lXxf86vm','-lXcursor','-lXi',
            '-lrt','-lm'
            ]
        }],
        ['OS=="mac"', {
          'include_dirs': [ '<!@(pkg-config glfw3 glew --cflags-only-I | sed s/-I//g)','-I<(ANTTWEAKBAR_ROOT)/include'],
          #'libraries': [ '<!@(pkg-config --libs glfw3 glew)', '-L<(ANTTWEAKBAR_ROOT)/lib', '-lAntTweakBar', '-framework OpenGL'],
          'libraries': [ '<!@(pkg-config --libs glfw3 glew)', '-L<(ANTTWEAKBAR_ROOT)/lib', '-lAntTweakBar', '-framework OpenGL'],
          'library_dirs': ['/usr/local/lib'],
        }],
        ['OS=="win"', {
            'include_dirs': [
              './deps/include',
              '~/.node-gyp/4.4.0/include/node'
              ],
            'library_dirs': [
              './deps/windows/lib/<(target_arch)',
              ],
            'libraries': [
              'FreeImage.lib',
              'AntTweakBar64.lib',
              'glfw3dll.lib',
              'glew32.lib',
              'opengl32.lib'
              ],
            'defines' : [
              'WIN32_LEAN_AND_MEAN',
              'VC_EXTRALEAN'
            ],
            'msvs_settings' : {
              'VCCLCompilerTool' : {
                'AdditionalOptions' : ['/O2','/Oy','/GL','/GF','/Gm-','/EHsc','/MT','/GS','/Gy','/GR-','/Gd']
              },
              'VCLinkerTool' : {
                'AdditionalOptions' : ['/OPT:REF','/OPT:ICF','/LTCG']
              },
            },
            'conditions': [
              ['target_arch=="ia32"', {
                'libraries': ['AntTweakBar.lib']
              }],
              ['target_arch=="x64"', {
                'libraries': ['AntTweakBar64.lib']
              }]
            ]
          }
        ]
      ]
    }
  ]
}
